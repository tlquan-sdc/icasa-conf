"""Edition-specific ICASA settings.

Update this file for each conference edition, then run:
    python build_site.py
"""

CONFERENCE = {
    "series_name": "ICASA",
    "full_name": "International Conference on AI-based Smart Agriculture in ASEAN",
    "year": 2027,
    "edition_number": "01",
    "edition_ordinal": "1st",
    "edition_word": "first",
    "edition_label": "Inaugural edition",
    "city": "Da Nang",
    "country": "VietNam",
    "region": "Central VietNam",
    "latitude": "16.0544",
    "longitude": "108.2022",
    "setting": "Han River",
    "conference_period": "18–20 May 2027",
    "submission_deadline": "1 January 2027",
    "timezone": "Asia/Ho_Chi_Minh",
    "timezone_label": "ICT",
    "organizer": "Software Development Centre (SDC), The University of Danang",
    "organizer_short": "SDC · The University of Danang",
    "organizer_url": "https://sdc.udn.vn/",
    "contact_email": "icasa.conf@sdc.udn.vn",
    "host_university": "The University of Danang",
    "site_url": "https://icasa-conf.org",
    "cmt_url": "",
    "publication": {
        "publisher": "Springer Nature",
        "series_short": "LNICST",
        "series_name": "Lecture Notes of the Institute for Computer Sciences, Social Informatics and Telecommunications Engineering",
        "series_url": "https://link.springer.com/series/8197",
        "indexing": ["Scopus"],
    },
    "hero_image": "assets/danang-hero-2027.webp",
    "social_image": "assets/danang-hero-2027.webp",
    "social_image_width": 2170,
    "social_image_height": 725,
    "logo_image": "assets/icasa-2027-logo.webp",
    # From 2028 onward, link each preserved edition here.
    # Example: {"year": 2027, "url": "archive/2027/"}
    "past_editions": [],
    # Copy optimized, real conference photos to assets/ and list them here.
    # The gallery remains hidden while this list is empty.
    "gallery": [
        # {
        #     "src": "assets/conference-opening.webp",
        #     "alt": "Delegates attending the ICASA opening session",
        #     "caption": "Opening session",
        #     "width": 1600,
        #     "height": 1067,
        # },
    ],
    "tracks": [
        {
            "title": "AI-based Smart Agriculture and Machine Learning",
            "description": "AI models, predictive analytics, farm intelligence and responsible decision-making.",
            "featured": True,
        },
        {
            "title": "Computer Vision, Remote Sensing and Crop Phenotyping",
            "description": "Imaging, satellite and UAV data, crop monitoring, yield estimation and disease detection.",
            "featured": True,
        },
        {
            "title": "Agricultural Biology and Computational Bioinformatics",
            "description": "Biological data analysis, systems biology and computational methods for agricultural research.",
            "featured": True,
        },
        {
            "title": "Plant Genomics, Smart Breeding and Biotechnology",
            "description": "Genomics, marker-assisted breeding, gene–environment interactions and crop improvement.",
            "featured": True,
        },
        {
            "title": "Agricultural Microbiology, Microbiomes and Biological Control",
            "description": "Plant–microbe interactions, soil microbiomes, beneficial organisms and biological protection.",
            "featured": False,
        },
        {
            "title": "Plant Health, Pathology and Precision Crop Protection",
            "description": "Pest and disease diagnosis, epidemiology and targeted crop-protection strategies.",
            "featured": False,
        },
        {
            "title": "IoT, Smart Sensors and Edge AI for Agriculture",
            "description": "Connected sensing, embedded intelligence, field monitoring and real-time control.",
            "featured": True,
        },
        {
            "title": "Agricultural Robotics, UAVs and Autonomous Systems",
            "description": "Field robots, drones, automation and intelligent agricultural machinery.",
            "featured": False,
        },
        {
            "title": "Soil, Water and Precision Nutrient Management",
            "description": "Soil health, irrigation, fertility assessment and site-specific input optimisation.",
            "featured": True,
        },
        {
            "title": "Climate-smart Agriculture and Environmental Sustainability",
            "description": "Climate resilience, resource efficiency, biodiversity and circular agricultural systems.",
            "featured": True,
        },
        {
            "title": "Smart Aquaculture, Livestock and Animal Health",
            "description": "Monitoring, welfare, feeding, disease prevention and intelligent production systems.",
            "featured": True,
        },
        {
            "title": "Agricultural Data, Digital Twins and Decision Support",
            "description": "Data integration, simulation, digital twins and explainable farm decision support.",
            "featured": False,
        },
        {
            "title": "Food Quality, Post-harvest Technology and Supply Chains",
            "description": "Food safety, quality assessment, traceability, storage and intelligent logistics.",
            "featured": False,
        },
        {
            "title": "ASEAN Agritech, Policy and Rural Innovation",
            "description": "Technology adoption, governance, entrepreneurship and inclusive regional development.",
            "featured": True,
        },
    ],
    "partner_logos": [
        {"src": "assets/udn-logo.webp", "width": 640, "height": 640},
        {"src": "assets/sdc-logo.jpg", "width": 500, "height": 500},
        {"src": "assets/eai-logo.png", "width": 1920, "height": 1080},
        {"src": "assets/springer-logo.webp", "width": 2400, "height": 663},
    ],
    "last_updated": "20 Oct 2026",
    "registration_fees": {
        "early_label": "Early registration (before 15 February 2027)",
        "late_label": "Late registration (16–25 February 2027)",
        "rows": [
            {
                "category": "Full-time research student",
                "early": "$200 (5,100,000 VND)",
                "late": "$250 (6,375,000 VND)",
            },
            {
                "category": "Faculty",
                "early": "$250 (6,375,000 VND)",
                "late": "$300 (7,650,000 VND)",
            },
            {
                "category": "Industry",
                "early": "$300 (7,650,000 VND)",
                "late": "$350 (8,925,000 VND)",
            },
        ],
    },
    "deadlines": [
        {"label": "Full paper submission deadline", "value": "1 January 2027", "iso": "2027-01-01"},
        {"label": "Acceptance notification", "value": "Coming soon"},
        {"label": "Early registration deadline", "value": "15 February 2027", "iso": "2027-02-15"},
        {"label": "Late registration deadline", "value": "25 February 2027", "iso": "2027-02-25"},
        {"label": "Camera-ready submission", "value": "March 2027", "iso": "2027-03"},
        {"label": "ICASA 2027 conference", "value": "18–20 May 2027", "iso": "2027-05-18"},
    ],
    "sponsors": [],
}
