"""Science-FM evidence (O8): Prithvi-EO-1.0-100M embeddings per chip,
representation-change per site, and cross-site nearest-neighbor analogs.

Model: ibm-nasa-geospatial/Prithvi-EO-1.0-100M (Apache-2.0), files under
demonstrator/prithvi/ (weights 453MB + prithvi_mae.py + config.json).
Chips are fed as single-frame inputs; the encoder interpolates its positional
embedding. Embedding = mean over final-layer patch tokens (cls excluded).

Writes fm fields into demonstrator/out/fm_evidence.json.
Usage: python3 demonstrator/prithvi_embed.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import torch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "prithvi"))
from prithvi_mae import PrithviMAE  # noqa: E402


def load_model():
    cfg = json.loads((HERE / "prithvi" / "config.json").read_text())["pretrained_cfg"]
    model = PrithviMAE(
        img_size=cfg["img_size"], patch_size=tuple(cfg["patch_size"]),
        num_frames=cfg["num_frames"], in_chans=cfg["in_chans"],
        embed_dim=cfg["embed_dim"], depth=cfg["depth"],
        num_heads=cfg["num_heads"],
        decoder_embed_dim=cfg["decoder_embed_dim"],
        decoder_depth=cfg["decoder_depth"],
        decoder_num_heads=cfg["decoder_num_heads"],
        mlp_ratio=cfg["mlp_ratio"],
    )
    sd = torch.load(HERE / "prithvi" / "Prithvi_EO_V1_100M.pt",
                    map_location="cpu", weights_only=False)
    if "model" in sd:
        sd = sd["model"]
    # checkpoint pos_embed is sized for 3 frames; forward interpolates, so
    # drop size-mismatched buffers rather than force-loading them
    model_sd = model.state_dict()
    sd = {k: v for k, v in sd.items()
          if k in model_sd and model_sd[k].shape == v.shape}
    missing = model.load_state_dict(sd, strict=False)
    print(f"loaded {len(sd)} tensors "
          f"(skipped {len(missing.missing_keys)} missing)")
    model.eval()
    return model, np.array(cfg["mean"]), np.array(cfg["std"])


@torch.no_grad()
def embed(model, chip, mean, std):
    # chips stored as reflectance/1e4; config stats are on the 1e4 scale
    x = chip * 10000.0
    x = (x - mean[:, None, None]) / std[:, None, None]
    t = torch.from_numpy(x.astype(np.float32)).unsqueeze(0).unsqueeze(2)
    feats = model.encoder.forward_features(t)[-1]  # (1, 1+tokens, 768)
    return feats[0, 1:, :].mean(dim=0).numpy()


def main() -> None:
    chips = np.load(HERE / "out" / "chips.npz")
    meta = json.loads((HERE / "out" / "chips_meta.json").read_text())
    model, mean, std = load_model()

    emb = {}
    for m in meta:
        for phase in ("before", "after"):
            key = f"{m['site_id']}_{phase}"
            emb[key] = embed(model, chips[key], mean, std)
            print(f"  embedded {key}")

    def cos(a, b):
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

    out = {}
    after_keys = [f"{m['site_id']}_after" for m in meta]
    for m in meta:
        sid = m["site_id"]
        d = 1.0 - cos(emb[f"{sid}_before"], emb[f"{sid}_after"])
        # analogs: nearest other sites in after-embedding space
        me = emb[f"{sid}_after"]
        sims = sorted(
            ((cos(me, emb[k]), k[:-6]) for k in after_keys
             if k != f"{sid}_after"),
            reverse=True,
        )[:3]
        out[sid] = {
            "repr_change_cosine_dist": d,
            "embedding_norm_before": float(np.linalg.norm(emb[f"{sid}_before"])),
            "embedding_norm_after": float(np.linalg.norm(emb[f"{sid}_after"])),
            "analogs": [{"ref": s, "similarity": round(v, 4),
                         "method": "cosine over Prithvi-EO-1.0-100M mean patch embeddings (after-scene)"}
                        for v, s in sims],
        }
    (HERE / "out" / "fm_evidence.json").write_text(
        json.dumps(out, indent=1), "utf-8"
    )
    np.savez_compressed(HERE / "out" / "embeddings.npz", **emb)
    print(f"FM evidence for {len(out)} sites")


if __name__ == "__main__":
    main()
