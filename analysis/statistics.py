import csv
import statistics
from collections import defaultdict, Counter

FULL_POSTS_FILE = "redsm5_posts.csv"
ANNOTATIONS_FILE = "redsm5_annotations.csv"
BDI_DSM5_MAPPING = {
    1: "DEPRESSED_MOOD",
    2: "DEPRESSED_MOOD",
    3: "WORTHLESSNESS",
    4: "ANHEDONIA",
    5: "WORTHLESSNESS",
    6: "WORTHLESSNESS",
    7: "WORTHLESSNESS",
    8: "WORTHLESSNESS",
    9: "SUICIDAL_THOUGHTS",
    10: "DEPRESSED_MOOD",
    11: "PSYCHOMOTOR",
    12: "ANHEDONIA",
    13: "COGNITIVE_ISSUES",
    14: "WORTHLESSNESS",
    15: "FATIGUE",
    16: "SLEEP_ISSUES",
    17: "DEPRESSED_MOOD",
    18: "APPETITE_CHANGE",
    19: "COGNITIVE_ISSUES",
    20: "FATIGUE",
    21: "ANHEDONIA",
}

DSM5_SYMPTOM_NAMES = set(BDI_DSM5_MAPPING.values())


def load_full_posts(path):
    posts = {}
    with open(path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            posts[row["post_id"]] = row["text"]
    return posts


def load_annotations(path):
    # For "posts per symptom" and hard negatives (status==1)
    post_to_symptoms = defaultdict(set)
    # For "all explanations" (status==1 or 0)
    post_to_all_annotations = defaultdict(list)
    with open(path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            post_id = row["post_id"]
            symptom = row["DSM5_symptom"]
            status = row["status"]
            if status == "1" and symptom in DSM5_SYMPTOM_NAMES:
                post_to_symptoms[post_id].add(symptom)
            if status in ("0", "1"):
                post_to_all_annotations[post_id].append((symptom, status))
    return post_to_symptoms, post_to_all_annotations


def print_statistics(post_ids, posts, post_to_symptoms, post_to_all_annotations):
    n_of_posts = len(post_ids)
    n_of_explanations = sum(len(post_to_all_annotations[pid]) for pid in post_ids)
    avg_explanations_per_post = n_of_explanations / n_of_posts if n_of_posts else 0
    n_of_hard_negatives = sum(1 for pid in post_ids if not post_to_symptoms[pid])
    post_lengths = [len(posts[pid].split()) for pid in post_ids]
    avg_length = sum(post_lengths) / n_of_posts
    min_length = min(post_lengths)
    max_length = max(post_lengths)
    median_length = statistics.median(post_lengths)
    std_dev_length = statistics.stdev(post_lengths) if n_of_posts > 1 else 0
    avg_symptoms_per_post = (
        sum(len(post_to_symptoms[pid]) for pid in post_ids) / n_of_posts
        if n_of_posts
        else 0
    )

    print(f"Total number of posts: {n_of_posts}")
    print(f"Total number of explanations (all status): {n_of_explanations}")
    print(f"Avg. number of explanations per post: {avg_explanations_per_post:.2f}")
    print(
        f"Avg. number of symptoms per post (status=1 only): {avg_symptoms_per_post:.2f}"
    )
    print(f"Number of hard negatives: {n_of_hard_negatives}")
    print(f"Avg. length of post (in words): {avg_length:.2f}")
    print(f"Median length of post (in words): {median_length}")
    print(f"Std. dev. of post length (in words): {std_dev_length:.2f}")
    print(f"Min. length of post (in words): {min_length}")
    print(f"Max. length of post (in words): {max_length}")


def print_symptom_distribution(post_to_symptoms):
    counter = Counter()
    for symptoms in post_to_symptoms.values():
        for s in symptoms:
            counter[s] += 1
    print("Posts per symptom (status=1 only):")
    for symptom, count in counter.most_common():
        print(f"  {symptom}: {count}")


def main():
    posts = load_full_posts(FULL_POSTS_FILE)
    post_to_symptoms, post_to_all_annotations = load_annotations(ANNOTATIONS_FILE)
    all_post_ids = list(posts.keys())
    print_statistics(all_post_ids, posts, post_to_symptoms, post_to_all_annotations)
    print()
    print_symptom_distribution(post_to_symptoms)


if __name__ == "__main__":
    main()
