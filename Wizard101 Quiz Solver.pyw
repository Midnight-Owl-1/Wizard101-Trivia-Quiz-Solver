#This program automatically logs into a Wizard101 account, and goes through each of the 10 trivia quizes per day, and answers them for you to get the free crowns
#You still need to complete the CAPTCHA for each quiz

#Takes a total of ~13 minutes to get your daily 100 crowns this way
#Since Crowns only cost $5USD per 2500, this method is only making you 20cents of crowns per day
#Since it takes you 13 mins to make 20 cents of value, you're valuing your time at 92 cents/hour

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from subprocess import CREATE_NO_WINDOW


from threading import Thread
from tkinter import *

import winsound

#These are all of the possible questions, and their associated answers
qna = {
    "What is Professor Falmea's favorite food?":"Pasta Arrabiata",
    "What hand does Lady Oriel hold her wand in?":"Trick question, she has a sword.",
    "What determines the colors of the manders in Krok?":"Where they come from and their school of focus.",
    "What school is the spell Dark Nova":"Shadow",
    "How long do you have to wait to join a new match after fleeing in PVP?":"5 minutes",
    "Who is in the top level of the Tower of the Helephant?":"Lyon Lorestriker",
    "What type of rank 8 spell is granted to Death students at level 58?":"Damage + DoT",
    "Which of these are not a lore spell?":"Fire Dragon",
    "Which of these is NOT a Zafaria Anchor Stone?":"Rasik Anchor Stone",
    "Who is the Bear King of Grizzleheim?":"Valgard Goldenblade",
    "What is the name of the secret society in Krokotopia":"Order of the Fang",
    "What is unique about Falmea's Classroom?":"There are scorch marks on the ceiling",
    "In Grizzleheim, the Ravens want to bring about:":"The Everwinter, to cover the world in ice:",
    "What is the name of the new dance added with Khrysalis?":"The bee dance",
    "What is the name of the book stolen from the Royal Museum?":"The Krokonomicon",
    "Which Aztecan ponders the Great Questions of Life?":"Philosoraptor",
    "What does the Time Ribbon Protect against?":"Time Flux",
    "What school is the Gurtok Demon focused on?":"Balance",
    "Shaka Zebu is known best as:":"The Greatest Living Zebra Warrior",
    "Who is Bill Tanner's sister?":"Sarah Tanner",
    "What is the shape on the weather vanes in the Shopping District?":"Half moon/moon",
    "What book was Anna Flameright accused of stealing?":"Advanced Flameology",
    "What level must you be to wear Dragonspyre crafted clothing?":"33",
    "What did Abigail Dolittle accuse Wadsworth of stealing?":"Genuine Imitation Golden Ruby",
    "What was the name of the powerful Grendel Shaman who sealed the runic doors?":"Thulinn",
    "Who Is NOT a member of the Council of Light?":"Cyrus Drake",
    "Sir Edward Halley is the Spiral's most famous:":"Aztecosaurologist",
    "Who is the King of the Burrowers?":"Pyat MourningSword",
    'Which Queen is mentioned in the Marleybone book "The Golden Age"?':"Ellen",
    "How many portal summoning candles are in the Burial Mound?":"Three",
    "Kirby Longspear was once a student of which school of magic?":"Death",
    "The Swordsman Destreza was killed by:":"A Gorgon",
    "Zafaria is home to what cultures?":"Gorillas, Zebras, Lions",
    "Which of these locations is not in Wizard City?":"Digmore Station",
    "What book does Professor Drake send you to the library to check out?":"Book on the Wumpus",
    "What is the title of the book that is floating around the Wizard City Library?":"Basic Wizarding & Proper Care of Familiars",
    "How many worlds of The Spiral are unlocked as of May 21st, 2014?":"12",
    "Why are the Gobblers so afraid to go home?":"Witches",
    "Merle Ambrose is originally from which world?":"Avalon",
    "Who sells Valentine's Day items in Wizard City?":"Valentina Heartsong",
    "Who is the Registrar of Pigswick Academy?":"Mrs. Dowager",
    "Who guards the entrance to Unicorn Way?":"Private Stillson",
    "What's the name of the balance tree?":"Niles",
    "What can be used to diminish the Nirini's powers in Krokotopia?":"Flame Gems",
    "Why are the pixies and faeries on Unicorn Way evil?":"Rattlebones corrupted them.",
    "Which below are NOT a type of Oni in MooShu?":"Ruby",
    'Who prophesizes this? "The mirror will break, The horn will call, From the shadows I strike , And the skies will fall..."':"Morganthe",
    "Who is the Nameless Knight?":"Sir Malory",
    "What color is the door inside the boys dormroom?":"Red",
    "What is the shape of the pink piece in potion motion?":"Heart",
    "Which one of these are not a symbol on the battle sigil?":"Wand",
    "What did Prospector Zeke lose track of in MooShu?":"Blue Oysters",
    "Which is the only school left standing in Dragonspyre?":"Fire",
    "Arthur Wethersfield is A:..":"Dog",
    "What course did Herold Digmoore study?":"Ancient Myths for Parliament",
    "What is flying around in Regent's Square?":"Newspapers",
    "What time of day is it always in Marleybone?":"Night",
    "What two names are on the Statues in the Marleybone cathedral?":"Saint Bernard and Saint Hubert",
    "What event is Abigail Doolittle sending out invitations for?":"Policeman's Ball",
    "What sort of beverage is served in Air Dales Hideaway?":"Root Beer",
    "What is a very common last name of the cats in Marleybone?":"O'Leary",
    "Who is not an officer you'll find around Marleybone?":"Officer Digmore",
    "What style of artifacts are in the Royal Museum?":"Krokotopian",
    "What initials were on the doctor's glove?":"XX",
    "Who is the dangerous criminal that is locked up, but escapes from Newgate Prison?":"Meowiarty",
    "What color are the Marleybone mailboxes?":"Red",
    "Which of these folks can you find in the Royal Museum?":"Clancy Pembroke",
    "Which is not a street in Regent's Square?":"Fleabitten Ave",
    "What is Sgt. Major Talbot's full name?":"Sylvester Quimby Talbot III",
    "What time does the clock always read in Marleybone?":"1:55",
    "Which symbol is not on the stained glass window in Regent's Square?":"A Tennis Ball",
    "What transports you from place to place in Marleybone?":"Hot Air Balloons",
    "What did Prospector Zeke lose in Marleybone?":"The Stray Cats",
    "Who is the Emperor of Mooshu's Royal Guard?":"Noboru Akitame",
    "In what world would you find the Spider Temple":"Zafaria",
    "Where is the only pure fire in the Spiral found?":"Wizard City",
    "King Neza is Zenzen Seven Star's:?":"Grandfather",
    "What was Ponce de Gibbon looking for in Azteca?":"The Water of Life",
    "In Reagent's Square, the Professor is standing in front of a:":"Telegraph Box",
    "Hrundle Fjord is part of what section of Grizzleheim?":"Wintertusk",
    "King Axaya Knifemoon needs what to unify the people around him?":"The Badge of Leadership",
    "Which villain terrorizes the fair maidens of Marleybone?":"Jaques the Scatcher",
    "Who gives you permission to ride the boat to the Krokosphinx?":"Sergent Major Talbot",
    "Who is the only person who knows how to enter the Tomb of Storms?":"Hetch Al'Dim",
    "Who was ordered to guard the Sword of Kings?":"The Knights of the Silver Rose",
    "Who did Falynn Greensleeves fall in love with?":"Sir Malick de Logres",
    "Who was the greatest Aquilan Gladiator of all time?":"Dimachaerus",
    "Who haunts the Night Warrens?":"Nosferabbit",
    "Who tells you how to get to Aquila?":"Harold Argleston",
    "Who takes you across the River of Souls?":"Charon",
    "Thaddeus Price is the Pigswick Academy Professor of what school?":"Tempest",
    "Who asks you to find Khrysanthemums?":"Eloise Merryweather",
    "What is used to travel to the Isle of Arachnis?":"Ice Archway",
    "Who makes the harpsicord for Shelus?":"Gretta Darkkettle",
    "Morganthe got the Horned Crown from the Spriggan:":"Gisela",
    "Sumner Fieldgold twice asks you to recover what for him?":"Shrubberies",
    "Who needs the healing potion from Master Yip?":"Binh Hoa",
    "Who is Haraku Yip's apprentice?":"Binh Hoa",
    'Who taunts you with: "Prepare to be broken, kid!"':"Clanker",
    "What badge do you earn by defeating 100 Samoorai?":"Yojimbo",
    "Who thinks you are there to take their precious feathers?":"Takeda Kanryu",
    "The Swallows of Caliburn migrate to Avalon from where each year?":"Zafaria and Marleybone",
    'Who tells you: "A shield is just as much a weapon as the sword."':"Mavra Flamewing",
    'Who tells you to speak these words only unto your mentor: "Meena Korio Jajuka!"':"Priya the Dryad",
    "Who tries to raise a Gorgon Army?":"Phorcys",
    'Who taunts you with: "Wizard, you will know the meaning of the word pain after we battle!"':"Aiuchi",
    "What special plant was Barley developing in his Garden?":"Cultivated Woodsmen",
    "Who helps Morganthe find the Horn of Huracan?":"Belloq",
    "Who taunts: Why I oughta knock you to the moon, you pesky little creep!":"Mugsy",
    "What does Silenus name you once you've defeated Hades?":"Glorious Golden Archon",
    "In Azteca, Morganthe enlisted the help of the:":"The Black Sun Necromancers",
    "Where has Pharenor been imprisoned?":"Skythorn Tower",
    "Who grants the first Shadow Magic spell?":"Sophia DarkSide",
    "Mortis can teach you this.":"Tranquilize",
    "What term best fits Sun Magic Spells?":"Enchantment",
    "What type of spells are Ice, Fire, and Storm?":"Elemental",
    "Who can teach you the Life Shield Spell?":"Sabrina Greenstar",
    "Mildred Farseer teaches you what kind of spell?":"Dispels",
    "What term best fits Star Magic Spells?":"Auras",
    "Who teaches you balance magic?":"Alhazred",
    "What isn't a shadow magic spell?":"Ebon Ribbons",
    "Which spell can't be cast while polymorphed as a Gobbler?":"Pie in the sky",
    "If you can cast Storm Trap, Wild Bolt, Catalan, and the Tempest spell, what are you polymorphed as?":"Ptera",
    "How many pips does it cost to cast Stormzilla?":"5",
    "Which spell would not be very effective when going for the elixir vitae Badge?":"Entangle",
    "Cassie the Ponycorn teaches this kind of spell:":"Prism",
    "What level of spell does Enya Firemoon Teach?":"80",
    "If you're a storm wizard with 4 power pips and 3 regular pips, how powerful would your supercharge charm be?":"110%",
    "How many pips does it cost to cast Dr. Von's Monster?":"9",
    "What does Forsaken Banshee do?":"375 damage plus a hex trap",
    "Which Fire spell both damages and heals over time?":"Power Link",
    "Ether Shield protects against what?":"Life and Death attacks",
    "Tish'Mah specializes in spells that mostly affect these:":"Minions",
    "Historian Gonzago is on a stage, who isn't in the audience?":"Giafra",
    'Historian Gonzago sends you on a "Paper Chase," who do you talk to during that quest?':"Magdalena",
    "How many Mechanical Birds do you collect in Sivella?":"5",
    "The Mooshu Tower in Sivella is a replica of what?":"Tower of Serenity",
    "What are Albus and Carbo?":"Armada Commanders",
    "What color of Windstone do you find in Marco Pollo's Tomb?":"Blue",
    "What kind of disguise do you wear in Sivella?":"Clockwork",
    "What shows Steed you're part of the Resistence?":"Amulet",
    "What type of boat do you use to get from the docks to Sivella?":"Gondola",
    "What type of item does Prospector Zeke want you to find in Valencia?":"Birds",
    "What's the name of a librarian in Sivella?":"Grassi",
    "Where do you find the Tomb of Marco Pollo?":"Granchia",
    "Which one isn't a Scholar by name?":"Caresini",
    "Which world doesn't have a pillar in Sivella?":"Monquista",
    "Who do you find in the Lecture Hall of Sivella?":"Ridolfo",
    "Who does Steed send you to speak to in Sivella?":"Thaddeus",
    "Who reads the inscription on Marleybone's Tower?":"Ratbeard",
    "Why does Steed want you to attack Armada Ships?":"Make a Disguise",
    "You need a good eye to save these in Granchia...":"Art Objects",
    "You won't find this kind of Armada Troop in Sivella!":"Battle Angel",
    "Who is the Fire School professor?":"Dalia Falmea",
    "What school does Malorn Ashthorn think is the best?":"Death",
    "What is the name of the bridge in front of the Cave to Nightside?":"Rainbow Bridge",
    "What does every Rotting Fodder in the Dark Caves carry with them?":"A spade",
    "Who is the Wizard City mill foreman?":"Sohomer Sunblade",
    "What is Diego's full name?":"Diego Santiago Quariquez Ramirez the Third",
    "What is something that the Gobblers are NOT stockpiling in Colossus Way?":"Broccoli",
    "Where is Sabrina Greenstar?":"Fairegrounds",
    "Who sang the Dragons, Tritons and Giants into existance?":"Bartleby",
    "What are the school colors of Balance?":"Tan and Maroon",
    "What are the main colors for the Myth School?":"Blue and Gold",
    "What school is all about Creativity?":"Storm",
    "What is the gemstone for Balance?":"Citrine",
    "Who resides in the Hedge Maze?":"Lady Oriel",
    "Who taught Life Magic before Moolinda Wu?":"Sylvia Drake",
    "Who is the Princess of the Seraphs?":"Lady Oriel",
    "What is the name of the school newspaper? Boris Tallstaff knows...":"Ravenwood Bulletin",
    "What is the name of the grandfather tree?":"Bartleby",
    "What is Mindy's last name (she's on Colossus Blvd)?":"Pixiecrown",
    "What is the name of the Ice Tree in Ravenwood?":"Kelvin",
    "What does Lethu Blunthoof says about Ghostmanes?":"You never can tell with them!",
    "Sir Reginal Baxby's cousin is:":"Mondli Greenhoof",
    "Baobab is governed by:":"A Council of three councilors.",
    "Who is the missing prince?":"Tiziri Silvertusk",
    "Umlilo Sunchaser hired who as a local guide?":"Msizi Redband",
    "Inyanga calls Umlio a:":"Fire feather",
    "The Fire Lion Ravagers are led by:":"Nergal the Burned Lion",
    "Unathi Nightrunner is:":"A councilor of Baobab.",
    "Who is not one of the Zebu Kings:":"Zaffe Zoffer",
    "Rasik Pridefall is:":"An Olyphant from Stone Town.",
    "Esop Thornpaw gives you a magic:":"Djembe Drum",
    "The Inzinzebu Bandits are harassing the good merchants in:":"Baobab Market",
    "Vir Goodheart is an assistant to:":"Rasik Pridefall",
    "Belloq is first found in:":"The Sook",
    "Zebu Blackstripes legendary blade was called:":"The Sword of the Duelist",
    "Jambo means:":"Hello.",
    "Zebu Blackstripes legendary blade was forged:":"In the halls of Valencia",
    "Koyate Ghostmane accuses the player of:":"Being a thief",
    "Who are Hannibal Onetusk's brother and co-pilot?":"Mago and Sobaka",
    "Zamunda's great assassin is known as:":"Karl the Jackal"
}

#These questions are known to be problematic, so we should just guess at the answer
problemQuestions = [
    "An unmodified Sun Serpent does what?"
]

#These are Direct URLS to the trivia quizes
triviaURLs = [
    "https://www.wizard101.com/quiz/trivia/game/wizard101-adventuring-trivia",
    "https://www.wizard101.com/quiz/trivia/game/wizard101-conjuring-trivia",
    "https://www.wizard101.com/quiz/trivia/game/wizard101-magical-trivia",
    "https://www.wizard101.com/quiz/trivia/game/wizard101-marleybone-trivia",
    "https://www.wizard101.com/quiz/trivia/game/wizard101-mystical-trivia",
    "https://www.wizard101.com/quiz/trivia/game/wizard101-spellbinding-trivia",
    "https://www.wizard101.com/quiz/trivia/game/wizard101-spells-trivia",
    "https://www.wizard101.com/quiz/trivia/game/pirate101-valencia-trivia",
    "https://www.wizard101.com/quiz/trivia/game/wizard101-wizard-city-trivia",
    "https://www.wizard101.com/quiz/trivia/game/wizard101-zafaria-trivia",
]

#This class takes care of the tkinter GUI window that the user communitcates with
class GUI():

    #Set up the GUI window
    def __init__(self):
        self.root = Tk()

        self.root.title('Wizard101 Quiz Solver')
        self.root.geometry('300x125')

        #IF someone presses the 'X' button, handle it using the windowClose function
        self.root.protocol('WM_DELETE_WINDOW', self.windowClose)

        #Give the window a custom crowns icon
        photo = PhotoImage(file = "icon.png")
        self.root.iconphoto(False, photo)

        self.startButton = Button(self.root, text="Start", command=self.startButtonPressed)
        self.startButton.place(x=120, y=80, width=60)

        self.descLabel = Label(self.root, text="Press the Start Button to start your daily quizes")
        self.descLabel.place(x=5,y=20, width=300)

    #If the user pressed the X button on the GUI window
    def windowClose(self):
        #self.descLabel['text'] = 'Exiting the program...' #This doesnt work because we're not running mainloop when this happens
        if(browser.driver != None):
            browser.destroy()
        self.root.destroy()
        quit()

    #Add the instance of the Browser class, which contains the Selenium webdriver (So that we can control it = start and stop it from this class)
    def addBrowser(self, browser):
        self.browser = browser

    #If the user presses the button, handle it
    def startButtonPressed(self):
        self.browser.ready = True
        self.startButton['state'] = DISABLED

        if(self.startButton['text'] == "Quit"):
            quit()

    #TK inter's mainloop - only start this after doing all of the other setup, because this haults the main thread
    def mainloop(self):
        self.root.mainloop()

#This class takes care of the Selenium Webdriver browser window, and also completes the actual trivia questions
class Browser(Thread):

    #Set this class up as a thread of it's own
    def __init__(self):
        super().__init__(daemon=True)
        self.ready = False
        self.driver = None

    #Add the instance of the GUI class, which contains the tk-inter window (So that we can control it = change description label, or button text from this class)
    def addGUI(self, gui):
        self.gui = gui

    #This sets up the Selenium webdriver chrome browser window, navigates to Wizard101, then accepts all cookies
    def driverSetup(self):
        #This diables chrome's "Do you want to save this password?" Popup
        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {"credentials_enable_service": False, "profile.password_manager_enabled": False})
        
        #Uses the latest chromedriver regardless of chrome's version
        chrome_service = ChromeService(ChromeDriverManager().install())
        #Disables opening up a command line window for chrome driver
        chrome_service.creationflags = CREATE_NO_WINDOW

        #Actually create the chrome window
        driver = webdriver.Chrome(service=chrome_service, options=options)
        self.driver = driver
        
        #Load up the first quiz url, just to get rid of the "Accept all Cookies" popup
        driver.get(triviaURLs[0])

        #Check if we need to "Accept cookies"
        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler'))).click()
        except:
            pass
        
        return driver

    #Attempt to log into Wizard101 using the credentials in 'account.txt'
    def login(self, driver):

        #This could error out if the account.txt file is not in the same working directory, OR if username or password is empty
        try:

            #Go into the account.txt file, and grab the first line (username), and second line (password)
            with open("account.txt","r") as f:
                lines = f.read().splitlines()
            username = lines[0][10:-1]
            password = lines[1][10:-1]

            if username == "" or password == "":
                raise Exception

        #If we have a problem with account.txt file, then alert the user, then gracefully close the program
        except:
            
            #Make the file again, just in case the .exe was moved
            with open("account.txt","w") as f:
                f.write("username=[xxx]\npassword=[xxx]")

            self.gui.descLabel['text'] = 'Please enter your Wizard101 Account login\n into account.txt (In same folder as this .exe),\nthen restart this program'
            self.gui.startButton['text'] = "Quit"
            self.gui.startButton['state'] = NORMAL
            winsound.Beep(830, 300)

            #Wait until user acknowledges the error by pressing the "Quit" button
            while(self.gui.startButton['state'] == NORMAL):
                time.sleep(0.5)
            
            self.gui.windowClose()
            
        #Input the username and password into the form, and press login
        driver.find_element(By.ID, 'loginUserName').send_keys(username)
        driver.find_element(By.ID, 'loginPassword').send_keys(password)
        driver.find_element(By.XPATH,'//input[@value="Login"]').click()

        #Ask the user if there has been any captcha request
        self.gui.descLabel['text'] = 'Check if there is Captcha to do\nIf so, do it, and complete the login.\nIf not, just press the "Continue" button here'
        self.gui.startButton['text'] = "Continue"
        self.gui.startButton['state'] = NORMAL
        winsound.Beep(830, 300)
        while(self.gui.startButton['state'] == NORMAL):
            time.sleep(0.5)

    #If we need to close the webbrowser window (ex. if user pressed "X" to GUI window)
    def destroy(self):
        self.driver.quit()

    #This is the main loop of this thread -> Where all of the actual work is done
    def run(self):

        #Wait until we're ready to start the quizes
        while(self.ready == False):
            time.sleep(1)

        #This try catch checks if the user has closed the webdriver browser
        try:
            #Set up the webbrowser window, then log in
            driver = self.driverSetup()
            self.login(driver)
            self.gui.descLabel['text'] = 'Completing your trivia questions...'

            #Go through all of the trivia quiz URLs one by one
            for url in triviaURLs:
                
                #Navigate the that url in the browser
                driver.get(url)
                
                time.sleep(1)

                #If we already did this quiz today, just skip onto the next one
                if "You exceeded the number of quizzes allowed today" in driver.page_source:
                    continue

                quizFinished = False
                #Keep going untill all of this quiz's questions are finished
                while quizFinished == False:

                    #Get the question from the webpage
                    question = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'quizQuestion')))

                    #Wait until all 4 potential answers are loaded in
                    potentialAnswers = []
                    while(len(potentialAnswers) != 4):
                        time.sleep(0.01)
                        potentialAnswers = driver.find_elements(By.XPATH, '//div[@class="answer fadeIn"]')
                    
                    #If this question is a known problematic question, just choose the first answer (Who cares if we get a couple wrong)
                    if(question.text in problemQuestions):
                        potentialAnswers[0].find_element(By.XPATH,'.//span[@class="answerBox"]').click()
                    
                    #If we have a question that is not in our list of questions and anwers, just choose the first answer (Who cares if we get a couple wrong)
                    elif (question.text not in qna.keys()):
                        potentialAnswers[0].find_element(By.XPATH,'.//span[@class="answerBox"]').click()
                    
                    #Our answer is among the options listed - Great
                    else:
                        foundAnswer = False
                        #Go through all of the potential answers
                        for p in potentialAnswers:
                            #If we find the correct answer, click the checkbox next to that answer
                            if (p.text == qna[question.text]):
                                p.find_element(By.XPATH,'.//span[@class="answerBox"]').click()
                                foundAnswer = True
                                break
                        
                        #If we couldn't find the answer for whatever reason, just choose the first answer (Who cares if we get a couple wrong)
                        if foundAnswer == False:
                            potentialAnswers[0].find_element(By.XPATH,'.//span[@class="answerBox"]').click()

                    #Wait until the "Next Question" button appears, and then click it
                    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "nextQuestion"))).click()

                    #Check if we finished the quiz
                    time.sleep(1)
                    if("YOU FINISHED THE" in driver.page_source):

                        #If this quiz is finished, then wait for the user to click the "Claim Crowns" button, and then complete the captcha
                        quizFinished = True
                        driver.find_element(By.XPATH,'//a[@class="kiaccountsbuttongreen"]').click()

                        #Alert the user that the quiz is done, and the CAPTCHA needs to be completed. Wait untill they press continue
                        self.gui.descLabel['text'] = 'In the browser, complete the CAPTCHA\n Then press the green "Claim your Reward" button.\nAfter you are done, press the "Continue" button here'
                        self.gui.startButton['text'] = "Continue"
                        self.gui.startButton['state'] = NORMAL
                        winsound.Beep(830, 300)
                        while(self.gui.startButton['state'] == NORMAL):
                            time.sleep(0.5)
            
            #Alert the user that all of the trivia quizes are completed for today
            winsound.Beep(830, 300)
            self.gui.descLabel['text'] = 'All 10 Trivia Quizes Completed'
            self.gui.startButton['text'] = "Quit"
            self.gui.startButton['state'] = NORMAL
        
        #The user has probably closed the webdriver browser
        except:
            self.driver = None
            self.gui.windowClose()


#This is where the main program starts
if __name__ == '__main__':
    
    gui = GUI()
    browser = Browser()

    gui.addBrowser(browser)
    browser.addGUI(gui)

    browser.start()
    gui.mainloop()
