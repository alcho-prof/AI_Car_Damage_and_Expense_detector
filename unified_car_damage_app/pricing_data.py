"""
Car parts baseline prices database by Manufacturer and Model.
Extends and cleans the pricing data from repo1 (sahilkhan-7/accident-damage-detection).
Prices are in INR baseline with dynamic currency conversion rates available.
"""

CURRENCY_RATES = {
    "INR": {"symbol": "₹", "rate": 1.0},
    "USD": {"symbol": "$", "rate": 0.012},
    "EUR": {"symbol": "€", "rate": 0.011},
    "GBP": {"symbol": "£", "rate": 0.0095}
}

CAR_PARTS_PRICES = {
    "HONDA": {
        "City": {"Bonnet": 15000, "Bumper": 10000, "Dickey": 8000, "Door": 20000, "Fender": 5000, "Light": 3000, "Windshield": 8000},
        "Civic": {"Bonnet": 18000, "Bumper": 12000, "Dickey": 10000, "Door": 24000, "Fender": 7000, "Light": 4000, "Windshield": 10000},
        "Accord": {"Bonnet": 22000, "Bumper": 15000, "Dickey": 13000, "Door": 28000, "Fender": 8000, "Light": 5000, "Windshield": 12000},
        "CR-V": {"Bonnet": 20000, "Bumper": 13000, "Dickey": 11000, "Door": 26000, "Fender": 7500, "Light": 4500, "Windshield": 11000},
        "Amaze": {"Bonnet": 12000, "Bumper": 8000, "Dickey": 6000, "Door": 18000, "Fender": 4000, "Light": 2500, "Windshield": 7000},
        "HR-V": {"Bonnet": 18000, "Bumper": 12000, "Dickey": 10000, "Door": 24000, "Fender": 7000, "Light": 4000, "Windshield": 10000}
    },
    "TOYOTA": {
        "Corolla": {"Bonnet": 20000, "Bumper": 13000, "Dickey": 11000, "Door": 26000, "Fender": 7500, "Light": 4500, "Windshield": 11000},
        "Camry": {"Bonnet": 22000, "Bumper": 15000, "Dickey": 13000, "Door": 28000, "Fender": 8000, "Light": 5000, "Windshield": 12000},
        "Fortuner": {"Bonnet": 25000, "Bumper": 17000, "Dickey": 15000, "Door": 30000, "Fender": 9000, "Light": 6000, "Windshield": 14000},
        "Innova": {"Bonnet": 23000, "Bumper": 16000, "Dickey": 14000, "Door": 29000, "Fender": 8500, "Light": 5500, "Windshield": 13000},
        "RAV4": {"Bonnet": 21000, "Bumper": 14000, "Dickey": 12000, "Door": 27000, "Fender": 8000, "Light": 4800, "Windshield": 11500},
        "Yaris": {"Bonnet": 18000, "Bumper": 12000, "Dickey": 10000, "Door": 24000, "Fender": 7000, "Light": 4000, "Windshield": 10000}
    },
    "HYUNDAI": {
        "i20": {"Bonnet": 15000, "Bumper": 10000, "Dickey": 8000, "Door": 20000, "Fender": 5000, "Light": 3000, "Windshield": 8000},
        "Creta": {"Bonnet": 18000, "Bumper": 12000, "Dickey": 10000, "Door": 24000, "Fender": 7000, "Light": 4000, "Windshield": 10000},
        "Verna": {"Bonnet": 16000, "Bumper": 11000, "Dickey": 9000, "Door": 22000, "Fender": 6000, "Light": 3500, "Windshield": 9000},
        "Venue": {"Bonnet": 17000, "Bumper": 11500, "Dickey": 9500, "Door": 23000, "Fender": 6500, "Light": 3750, "Windshield": 9500},
        "Tucson": {"Bonnet": 20000, "Bumper": 13000, "Dickey": 11000, "Door": 26000, "Fender": 7500, "Light": 4500, "Windshield": 11000}
    },
    "MARUTI SUZUKI": {
        "Swift": {"Bonnet": 10000, "Bumper": 7000, "Dickey": 5000, "Door": 15000, "Fender": 3000, "Light": 2000, "Windshield": 6000},
        "Baleno": {"Bonnet": 12000, "Bumper": 8000, "Dickey": 6000, "Door": 18000, "Fender": 4000, "Light": 2500, "Windshield": 7000},
        "Vitara Brezza": {"Bonnet": 14000, "Bumper": 9000, "Dickey": 7000, "Door": 20000, "Fender": 4500, "Light": 2800, "Windshield": 8000},
        "Grand Vitara": {"Bonnet": 18000, "Bumper": 12000, "Dickey": 10000, "Door": 24000, "Fender": 7000, "Light": 4000, "Windshield": 10000},
        "Ertiga": {"Bonnet": 16000, "Bumper": 11000, "Dickey": 9000, "Door": 22000, "Fender": 6000, "Light": 3500, "Windshield": 9000}
    },
    "FORD": {
        "Mustang": {"Bonnet": 32000, "Bumper": 22000, "Dickey": 18000, "Door": 38000, "Fender": 12000, "Light": 9000, "Windshield": 18000},
        "Explorer": {"Bonnet": 26000, "Bumper": 18000, "Dickey": 15000, "Door": 32000, "Fender": 10000, "Light": 7000, "Windshield": 15000},
        "F-150": {"Bonnet": 30000, "Bumper": 20000, "Dickey": 16000, "Door": 35000, "Fender": 11000, "Light": 8000, "Windshield": 16000},
        "EcoSport": {"Bonnet": 17000, "Bumper": 11000, "Dickey": 9000, "Door": 22000, "Fender": 6000, "Light": 3500, "Windshield": 9000}
    },
    "BMW": {
        "3 Series": {"Bonnet": 42000, "Bumper": 30000, "Dickey": 24000, "Door": 48000, "Fender": 16000, "Light": 18000, "Windshield": 24000},
        "5 Series": {"Bonnet": 48000, "Bumper": 35000, "Dickey": 28000, "Door": 55000, "Fender": 19000, "Light": 22000, "Windshield": 28000},
        "X3 / X5": {"Bonnet": 50000, "Bumper": 38000, "Dickey": 30000, "Door": 58000, "Fender": 20000, "Light": 24000, "Windshield": 30000}
    },
    "GENERIC VEHICLE": {
        "Standard Sedan": {"Bonnet": 16000, "Bumper": 11000, "Dickey": 9000, "Door": 22000, "Fender": 6000, "Light": 3500, "Windshield": 9000},
        "Compact SUV": {"Bonnet": 18000, "Bumper": 12500, "Dickey": 10000, "Door": 24000, "Fender": 7000, "Light": 4000, "Windshield": 10500},
        "Luxury Vehicle": {"Bonnet": 35000, "Bumper": 25000, "Dickey": 20000, "Door": 40000, "Fender": 14000, "Light": 12000, "Windshield": 20000}
    }
}

DEFAULT_PART_PRICE = {
    "Bonnet": 16000,
    "Bumper": 11000,
    "Dickey": 9000,
    "Door": 22000,
    "Fender": 6000,
    "Light": 3500,
    "Windshield": 9000
}

# Labor and painting rates (INR baseline)
BASE_LABOR_PAINT_RATE = {
    "Minor": {"labor_hours": 2.5, "hourly_rate": 1200, "paint_material": 2000},
    "Moderate": {"labor_hours": 5.0, "hourly_rate": 1400, "paint_material": 4500},
    "Severe": {"labor_hours": 9.0, "hourly_rate": 1600, "paint_material": 8000}
}
