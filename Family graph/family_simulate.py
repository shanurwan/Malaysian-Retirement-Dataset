import pandas as pd
import random
import uuid

random.seed(1140)


NUM_ADULTS = 1000
P_MARRIED = 0.75
CHILDREN_RANGE = (0, 4)
CHILD_AGE_RANGE = (18, 35)
AGE_GAP_RANGE = (3, 5)


def generate_id():
    return str(uuid.uuid4())

def generate_adult():
    return {
        "id": generate_id(),
        "type": "adult",
        "age": random.randint(50, 60),
        "gender": random.choice(["M", "F"]),
        "state": random.choice(["Selangor", "KL", "Penang", "Johor", "Sabah", "Sarawak"]),
    }

def generate_child():
    return {
        "id": generate_id(),
        "type": "child",
        "age": random.randint(*CHILD_AGE_RANGE),
        "gender": random.choice(["M", "F"]),
        "state": random.choice(["Selangor", "KL", "Penang", "Johor", "Sabah", "Sarawak"]),
    }

adults = [generate_adult() for _ in range(NUM_ADULTS)]
unmarried_adults = adults.copy()
married_pairs = []


while len(unmarried_adults) >= 2 and len(married_pairs) < int(P_MARRIED * NUM_ADULTS / 2):
    male = next((p for p in unmarried_adults if p['gender'] == 'M'), None)
    female = next((p for p in unmarried_adults if p['gender'] == 'F'), None)
    
    if male and female:
       
        age_gap = random.randint(*AGE_GAP_RANGE)
        male['age'] = min(60, max(50, female['age'] + age_gap))
        married_pairs.append((male, female))
        unmarried_adults.remove(male)
        unmarried_adults.remove(female)
    else:
        break


nodes = []
edges = []


nodes.extend(adults)


for husband, wife in married_pairs:
    
    edges.append({"from_id": husband["id"], "to_id": wife["id"], "relation": "MARRIED_TO"})
    edges.append({"from_id": wife["id"], "to_id": husband["id"], "relation": "MARRIED_TO"})
    
    num_kids = random.randint(*CHILDREN_RANGE)
    for _ in range(num_kids):
        child = generate_child()
        nodes.append(child)
        
        edges.append({"from_id": husband["id"], "to_id": child["id"], "relation": "HAS_CHILD"})
        edges.append({"from_id": wife["id"], "to_id": child["id"], "relation": "HAS_CHILD"})
        
        if random.random() < 0.6:
            supported_parent = random.choice([husband, wife])
            edges.append({"from_id": child["id"], "to_id": supported_parent["id"], "relation": "SUPPORTS"})


nodes_df = pd.DataFrame(nodes)
edges_df = pd.DataFrame(edges)

nodes_df.to_csv("nodes.csv", index=False)
edges_df.to_csv("edges.csv", index=False)


