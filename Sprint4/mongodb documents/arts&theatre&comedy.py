import random
import json
import requests
from datetime import datetime, timedelta

UNSPLASH_ACCESS_KEY = "EY8Rq3I7DfDGBONe7RfMNn4WXf2cUtJWwoXDL_ZUuGo"

# Define pre-determined event IDs
event_ids = [2, 8, 17, 18, 22, 26, 32, 39, 47, 48, 50, 53, 57, 62, 63, 66, 67, 68, 76, 77, 79, 88, 89]

# Define possible values for random generation
# names = [
#     "Alex Rivera", "Jamie Lee", "Taylor Reese", "Jordan Monroe", "Robin Evans", 
#     "Morgan Swift", "Drew Hart", "Casey Parker", "Avery Quinn", "Sage Brooks"
# ]
artist_profiles = [
    {
        "name": "Alex Rivera",
        "website": "https://alexrivera-arts.com",
        "wikipediaLink": "https://wikipedia.org/wiki/Alex_Rivera"
    },
    {
        "name": "Jamie Lee",
        "website": "https://jamielee-comedy.com",
        "wikipediaLink": "https://wikipedia.org/wiki/Jamie_Lee"
    },
    {
        "name": "Taylor Reese",
        "website": "https://taylorreese-theater.org",
        "wikipediaLink": "https://wikipedia.org/wiki/Taylor_Reese"
    },
    {
        "name": "Jordan Monroe",
        "website": "https://jordanmonroe.com",
        "wikipediaLink": "https://wikipedia.org/wiki/Jordan_Monroe"
    },
    {
        "name": "Robin Evans",
        "website": "https://robinsartspace.com",
        "wikipediaLink": "https://wikipedia.org/wiki/Robin_Evans"
    },
    {
        "name": "Morgan Swift",
        "website": "https://morganswift-performer.info",
        "wikipediaLink": "https://wikipedia.org/wiki/Morgan_Swift"
    },
    {
        "name": "Drew Hart",
        "website": "https://drewhart-standup.com",
        "wikipediaLink": "https://wikipedia.org/wiki/Drew_Hart"
    },
    {
        "name": "Casey Parker",
        "website": "https://caseyparker.com",
        "wikipediaLink": "https://wikipedia.org/wiki/Casey_Parker"
    },
    {
        "name": "Avery Quinn",
        "website": "https://averyquinn-theatre.org",
        "wikipediaLink": "https://wikipedia.org/wiki/Avery_Quinn"
    },
    {
        "name": "Sage Brooks",
        "website": "https://sagebrooks-art.com",
        "wikipediaLink": "https://wikipedia.org/wiki/Sage_Brooks"
    }
]

bios = [
    "An emerging artist known for their striking use of color and abstract forms.",
    "A comedian who brings real-world issues to the stage with a humorous twist.",
    "A theater actor with a background in both classical and modern drama.",
    "An interdisciplinary artist exploring themes of identity and nature.",
    "A stand-up comedian with a sharp, observational humor style.",
    "A stage performer celebrated for their high-energy, immersive shows.",
    "An abstract artist whose work challenges traditional boundaries of form.",
    "A performer known for blending satire and storytelling.",
    "A veteran theater actor revered for their versatility on stage.",
    "An experimental artist pushing the limits of visual and performance art."
]
# websites = [
#     "https://alexrivera-arts.com", "https://jordanmonroe-comedy.com", 
#     "https://averyquinn-theatre.org", "https://tayloreese-studio.net", 
#     "https://sagebrooks-art.com", "https://morganswift-performer.info",
#     "https://drew-hart-standup.com", "https://robinevans-performances.org"
# ]
# wikipedia_links = [
#     "https://wikipedia.org/wiki/Alex_Rivera", "https://wikipedia.org/wiki/Jamie_Lee",
#     "https://wikipedia.org/wiki/Taylor_Reese", "https://wikipedia.org/wiki/Jordan_Monroe",
#     "https://wikipedia.org/wiki/Robin_Evans", "https://wikipedia.org/wiki/Morgan_Swift",
#     "https://wikipedia.org/wiki/Drew_Hart", "https://wikipedia.org/wiki/Casey_Parker"
# ]

# Define artist types
artist_types = ["musician", "opera", "comedian", "painter", "theater", "sculptor"]

def get_unsplash_image_url(keyword):
    """Fetch a random image URL from Unsplash based on the keyword."""
    url = f"https://api.unsplash.com/photos/random?query={keyword}&client_id={UNSPLASH_ACCESS_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["urls"]["regular"]  # Get a suitable image size URL
    else:
        # Fallback image if API call fails
        return "https://via.placeholder.com/400"

def generate_random_event_data(event_id):
    # Randomly choose values for each field
    artist_profile = random.choice(artist_profiles)
    performer_name = artist_profile["name"]
    performer_website = artist_profile["website"]
    performer_wikipedia = artist_profile["wikipediaLink"]
    # performer_name = random.choice(names)
    performer_bio = random.choice(bios)
    # performer_website = random.choice(websites)
    # performer_wikipedia = random.choice(wikipedia_links)
    performer_type = random.choice(artist_types)  # Choose a random artist type
    
    # Use Unsplash to get a random image URL based on the performer type
    event_image = get_unsplash_image_url(keyword=performer_type)
    
    # Set last updated to a random date within the last year
    last_updated_date = datetime.now() - timedelta(days=random.randint(0, 365))
    
    # Create event data dictionary
    event_data = {
        "number": event_id,
        "performer": {
            "type": performer_type,
            "name": performer_name,
            "bio": performer_bio,
            "image": event_image,
            "website": performer_website,
            "wikipediaLink": performer_wikipedia
        },
        "images": event_image,
        "last_updated": last_updated_date.strftime("%Y-%m-%d")
    }
    
    return event_data

# Generate a list of event data records using the predefined event IDs
event_data_list = [generate_random_event_data(event_id) for event_id in event_ids]

# Convert list to JSON format for easier saving or printing
event_data_json = json.dumps(event_data_list, indent=2)
print(event_data_json)
