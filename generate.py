import json
import random

# Base lists built from the linguistic profile of Delta State names (Urhobo, Isoko, Itsekiri, Ijaw, Anioma)
first_names = [
    "Elohor", "Oghenekevwe", "Kevwe", "Onome", "Oghenevo", "Ese", "Efe", "Othuke", "Blessing", "Favour",
    "Gloria", "Dupe", "Florence", "Bridget", "Mercy", "Lovet", "Anthonia", "Ada", "Ruth", "Happy",
    "Helen", "Chika", "Mesufe", "Amechi", "Collins", "Edina", "Franklin", "Albert", "George", "Stephen",
    "Samson", "Owhowho", "Ishola", "Okotete", "Ediri", "Arubasa", "Umukoro", "Akpos", "Yaqub", "Lawal"
]

last_names = [
    "ELOHOR", "ADUDO", "OGHENEKEVWE", "MARVELOUS", "Aguin", "Josephine", "U..", "PRECIOUS", "OVWIOmottho",
    "FAVOUR", "HAPPY", "OSCAR", "ORJI", "FAITH", "Sulaiman", "Job", "vwede", "NELSON", "Alfred",
    "DENNIS", "CORDELIA", "Maraba", "EJEBEI", "JOHNBULL", "AGBAJE", "GABRIEL ISAIAH", "BONNY", "OLUWA Tope",
    "Rose", "OGROYE", "KEVWE", "KUGBEDI", "Edugbo", "RITA", "KOSIN", "Olalekan", "Lucky", "Akunne",
    "Godwin", "Oje", "Uwhojor", "OKUOLOLO", "OKPORO", "Inoto", "Ola", "OMOKUGHEGBE", "ESTHER", "SAMUEL",
    "Igapu", "oborhoghe", "POTOKRI", "Alico"
]

def generate_phone():
    # Nigerian active mobile prefix syntax
    prefixes = ["0803", "0806", "0703", "0706", "0813", "0816", "0903", "0906", "0805", "0807", "0705", "0815", "0811", "0905", "0802", "0808", "0701", "0708", "0812", "0902", "0907", "0809", "0817", "0818", "0909"]
    return random.choice(prefixes) + "".join(str(random.randint(0, 9)) for _ in range(7))

def randomize_casing(text):
    # Mimics human typing anomalies found in the sample file
    rand = random.random()
    if rand < 0.4:
        return text.upper()
    elif rand < 0.7:
        return text.lower()
    return text.title()

def generate_dataset(total_records=60000):
    dataset = []
    seen_phones = set()
    
    print(f"Generating {total_records} records...")
    
    while len(dataset) < total_records:
        first = randomize_casing(random.choice(first_names))
        last = randomize_casing(random.choice(last_names))
        phone = generate_phone()
        
        # Enforce unique phone numbers
        if phone not in seen_phones:
            seen_phones.add(phone)
            dataset.append({
                "firstName": first,
                "lastName": last,
                "phone": phone
            })
            
    return dataset

if __name__ == "__main__":
    output_filename = "deltan_names_phone_sample_7k.json"
    data = generate_dataset(7000)
    
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        
    print(f"Success! Exactly {len(data)} records saved directly to '{output_filename}'")
