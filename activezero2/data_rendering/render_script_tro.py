import os
import os.path as osp
import sys
import time

import numpy as np
import sapien.core as sapien
from loguru import logger
from path import Path
import json

CUR_DIR = os.path.dirname(__file__)
REPO_ROOT = os.path.abspath(osp.join(osp.dirname(__file__), ".."))
sys.path.insert(0, REPO_ROOT)
from data_rendering.render_scene_tro import render_gt_depth_label, render_scene, SCENE_DIR
from data_rendering.utils.render_utils import load_pickle

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--sub", type=int, required=True)
    parser.add_argument("--total", type=int, required=True)
    parser.add_argument("--target-root", type=str, required=True)
    parser.add_argument("--rand-pattern", action="store_true")
    parser.add_argument("--fixed-angle", action="store_true")
    parser.add_argument("--rand-lighting", action="store_true")
    parser.add_argument("--primitives", action="store_true", help="use primitives")
    parser.add_argument("--primitives-v2", action="store_true", help="use primitives v2")
    parser.add_argument("--thin", action="store_true", help="use thin primitives")
    parser.add_argument("--rand-table", action="store_true", help="use random material for table")
    parser.add_argument("--rand-env", action="store_true", help="use random environment map")
    parser.add_argument("--trans-prob", type=float, required=True)
    parser.add_argument("--spp", type=int, required=True)
    parser.add_argument("--denoise", action="store_true")
    parser.add_argument("--material", type=str, required=True)
    args = parser.parse_args()

    assert args.fixed_angle and (not args.rand_pattern) and (not args.rand_lighting) and (not args.primitives) and (
        not args.primitives_v2) and (not args.thin) and (not args.rand_table) and (not args.rand_env)
    spp = args.spp
    num_view = 21

    repo_root = REPO_ROOT
    target_root = args.target_root
    data_root = osp.join(args.target_root, "data")
    Path(data_root).makedirs_p()

    timestamp = time.strftime("%y-%m-%d_%H-%M-%S")
    name = "render_" + target_root.split("/")[-1]
    filename = f"log.render.sub{args.sub:02d}.tot{args.total}.{timestamp}.txt"
    # set up logger
    logger.remove()
    fmt = (
        f"<green>{{time:YYYY-MM-DD HH:mm:ss.SSS}}</green> | "
        f"<cyan>{name}</cyan> | "
        f"<lvl>{{level}}</lvl> | "
        f"<lvl>{{message}}</lvl>"
    )

    # logger to file
    log_file = Path(target_root) / filename
    logger.add(log_file, format=fmt)

    # logger to std stream
    logger.add(sys.stdout, format=fmt)
    logger.info(f"Args: {args}")

    if args.primitives or args.primitives_v2 or args.thin:
        total_scene = 2000
        scene_names = np.arange(total_scene)
        sub_total_scene = len(scene_names) // args.total
        sub_scene_list = (
            scene_names[(args.sub - 1) * sub_total_scene: args.sub * sub_total_scene]
            if args.sub < args.total
            else scene_names[(args.sub - 1) * sub_total_scene:]
        )
    else:
        total_scene = 1000
        scene_names = np.arange(total_scene)
        sub_total_scene = len(scene_names) // args.total
        sub_scene_list = []
        if args.sub < args.total:
            for s in scene_names[(args.sub - 1) * sub_total_scene: args.sub * sub_total_scene]:
                sub_scene_list.append(f"0-{s}")
                sub_scene_list.append(f"1-{s}")
        else:
            for s in scene_names[(args.sub - 1) * sub_total_scene:]:
                sub_scene_list.append(f"0-{s}")
                sub_scene_list.append(f"1-{s}")

    logger.info(f"Generating {len(sub_scene_list)} scenes from {sub_scene_list[0]} to {sub_scene_list[-1]}")

    # build scene
    sim = sapien.Engine()
    sim.set_log_level("warning")
    sapien.KuafuRenderer.set_log_level("warning")

    render_config = sapien.KuafuConfig()
    render_config.use_viewer = False
    render_config.use_denoiser = args.denoise
    render_config.spp = spp
    render_config.max_bounces = 8

    renderer = sapien.KuafuRenderer(render_config)
    sim.set_renderer(renderer)

    for sc in sub_scene_list:
        done = True
        for v in range(num_view):
            if not osp.exists(osp.join(data_root, f"{sc}-{v}/{spp:04d}_irR_{args.material}_den{args.denoise}_half.png")):
                done = False
                break
        if done:
            logger.info(f"Skip scene {sc} rendering")
            continue

        logger.info(f"Rendering scene {sc}")
        render_scene(
            sim=sim,
            renderer=renderer,
            denoise=args.denoise,
            material_name=args.material,
            scene_id=sc,
            repo_root=repo_root,
            target_root=data_root,
            spp=spp,
            num_views=num_view,
            rand_pattern=args.rand_pattern,
            fixed_angle=args.fixed_angle,
            primitives=args.primitives,
            primitives_v2=args.primitives_v2,
            thin=args.thin,
            rand_lighting=args.rand_lighting,
            rand_table=args.rand_table,
            rand_env=args.rand_env,
            trans_prob=args.trans_prob,
        )

    renderer = None
    sim = None

    sim_vk = sapien.Engine()
    sim_vk.set_log_level("warning")

    renderer = sapien.VulkanRenderer(offscreen_only=True)
    renderer.set_log_level("warning")
    sim_vk.set_renderer(renderer)

    for sc in sub_scene_list:
        if osp.exists(osp.join(data_root, f"{sc}-{num_view - 1}/depthR_colored.png")):
            logger.info(f"Skip scene {sc} gt depth and seg")
            continue
        logger.info(f"Generating scene {sc} gt depth and seg")
        render_gt_depth_label(
            sim=sim_vk,
            renderer=renderer,
            scene_id=sc,
            repo_root=repo_root,
            target_root=data_root,
            spp=spp,
            num_views=num_view,
            rand_pattern=args.rand_pattern,
            fixed_angle=args.fixed_angle,
            primitives=args.primitives,
            primitives_v2=args.primitives_v2,
            thin=args.thin,
        )
    exit(0)