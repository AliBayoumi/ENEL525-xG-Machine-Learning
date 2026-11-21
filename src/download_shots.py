"""Download every shot from StatsBomb's free men's competitions and save to data/shots.csv."""
import os
import warnings
import pandas as pd
from statsbombpy import sb

warnings.filterwarnings("ignore")  # hides the "no login" warning

OUT_DIR = "data/raw"
os.makedirs(OUT_DIR, exist_ok=True)

# Only the columns we need: what happened BEFORE the shot, plus the outcome (label)
COLUMNS = ["match_id", "period", "minute", "team", "player", "location",
           "play_pattern", "shot_type", "shot_body_part", "shot_technique",
           "under_pressure", "shot_first_time", "shot_outcome", "shot_statsbomb_xg"]

comps = sb.competitions()
comps = comps[comps["competition_gender"] == "male"]

for _, c in comps.iterrows():
    name = f"{c['competition_name']} {c['season_name']}".replace("/", "-")
    path = os.path.join(OUT_DIR, f"{name}.csv")
    if os.path.exists(path):          # lets you re-run safely if it crashes midway
        print(f"skip {name} (already downloaded)")
        continue

    matches = sb.matches(competition_id=c["competition_id"], season_id=c["season_id"])
    frames = []
    for i, match_id in enumerate(matches["match_id"], 1):
        events = sb.events(match_id=match_id)
        shots = events[events["type"] == "Shot"].reindex(columns=COLUMNS)
        shots["match_id"] = match_id
        frames.append(shots)
        print(f"\r{name}: {i}/{len(matches)} matches", end="")

    df = pd.concat(frames)
    df["competition"] = c["competition_name"]
    df["season"] = c["season_name"]
    df.to_csv(path, index=False)
    print(f"\n  saved {len(df)} shots")

# Combine every competition into one file
all_shots = pd.concat(pd.read_csv(os.path.join(OUT_DIR, f)) for f in os.listdir(OUT_DIR))
all_shots.to_csv("data/shots.csv", index=False)
print(f"Done: {len(all_shots)} shots from {all_shots['match_id'].nunique()} matches")