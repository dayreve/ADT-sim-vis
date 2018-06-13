import random
from datetime import date, datetime, timedelta

male_names = ['Maurice','Antonio','Vern','Rory','Odis','Clarence','Bradford','Michael','Gerry','Peter','Maria','Long','Alden','Bruno','Lynn','Carmine','Wallace','Abram','Leroy','Edgar','Asa','Fredrick','Nicholas','Jerrell','Rafael','Irving','Mac','Rolando','Jules','Chester','Jeremy','Osvaldo','Darwin','Hans','Deangelo','Val','Otha','Elisha','Jose','Renato','Gayle','Art','Van','Micah','Nick','Pete','Aubrey','Felton','Sidney','Angel']
female_names = ['Mae','Catherina','Yung','Claretta','Luetta','Edwina','Lahoma','Melodi','Barb','Deandra','Mao','Shelia','Sondra','Raymonde','Sharda','Gita','Bonnie','Brittny','Roma','Janiece','Phebe','Eloisa','Keila','Kam','Kera','Brigette','Torrie','Lia','Lizabeth','Drema','Lourie','Zoe','Allena','Kasha','Buena','Tu','Patria','Dina','Jann','Sherie','Katina','Franchesca','Ardis','Sunshine','Shaneka','Adria','Alysia','Renae','Mabelle','Elicia']
surnames = ['Clark','Ramirez','Oliver','Quinn','Costa','Black','Kelley','Leach','Mullen','Parrish','Pitts','Powers','Stout','Phelps','Bernard','Chaney','Harrison','Daniel','Ritter','Madden','Robertson','Davis','Cunningham','Hammond','Leon','Cole','Marquez','Dalton','Savage','Rasmussen','Cabrera','Wheeler','Blevins','Krause','Holden','Barry','Duran','Mata','Obrien','Schmidt','Suarez','Stanton','Lloyd','Duarte','Bush','Bautista','Arias','Thomas','Bender','Thompson','Cline','Bradley','Moreno','Orr','Weber','Rocha','Martinez','Clarke','Page','Curtis','Myers','Le','Sherman','Mayer','Conrad','Winters','Chambers','Baird','Orozco','Gomez','Herring','Robbins','Gentry','Rich','Blankenship','Frederick','Aguirre','Donovan','Maynard','Cantrell','Hoover','Mcbride','Hamilton','Pierce','Walsh','Wilkinson','Dickerson','Stanley','Montoya','Daniels','Walton','Pratt','Fisher','Shaffer','Allen','Baxter','Bailey','Hobbs','White','Bean']

def random_gender():
    return random.choice(['male', 'female'])

def random_male():
    return random.choice(male_names)

def random_female():
    return random.choice(female_names)

def random_surname():
    return random.choice(surnames)

def random_dob():
    year = timedelta(days=365)
    return str(date.today() - year*90 + random.random()*(year*90))

def random_edd():
    day = timedelta(days=1)
    return str(date.today() + random.random()*(day*7))

def random_news():

    x = random.random()

    if x < 0.6:
        return random.choice(range(0, 5))
    elif x < 0.9:
        return random.choice(range(5, 7))
    else:
        return random.choice(range(7, 13))
