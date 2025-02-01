import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('cyber_defender.db')
cursor = conn.cursor()

# Create Users Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    Username TEXT NOT NULL,
    Email TEXT NOT NULL UNIQUE,
    PasswordHash TEXT NOT NULL
)
''')
# Delete all existing users to ensure a clean start
cursor.execute("DELETE FROM Users")

# Create Scores Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Scores (
    ScoreID INTEGER PRIMARY KEY AUTOINCREMENT,
    UserID INTEGER,
    Stage INTEGER,
    Score INTEGER,
    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
)
''')

# Create Questions Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Questions (
    QuestionID INTEGER PRIMARY KEY AUTOINCREMENT,
    Stage INTEGER NOT NULL,
    QuestionText TEXT NOT NULL,
    OptionA TEXT NOT NULL,
    OptionB TEXT NOT NULL,
    OptionC TEXT NOT NULL,
    OptionD TEXT NOT NULL,
    CorrectAnswer TEXT NOT NULL
)
''')

# New Sample Questions
sample_questions = [
    # Stage 01 - Phishing
    (1, "You receive an email claiming to be from a popular delivery service stating that there’s a 'problem' with your recent delivery. It asks you to click a link to update your address and payment information. You’re not expecting any delivery. What should you do first?", 
        "Click on the link and immediately provide the requested details.", 
        "Delete the email without reading further.", 
        "Verify the email by contacting the delivery service’s official customer support or checking your official order history.", 
        "Forward the email to your friends and ask them if they’ve experienced the same.", 
        "C"),
        
    (1, "A bank you have never used sends you an email requesting to 'confirm your account details' to avoid closure. How should you react?", 
        "Reply with your personal information so they don’t close your account.", 
        "Ignore it because you know you don’t have an account with that bank.", 
        "Click the link to see what happens and if it looks real.", 
        "Immediately forward it to your bank’s email address to confirm legitimacy.", 
        "B"),
        
    (1, "A pop-up on a social media website claims you’ve won a $500 gift card. It prompts you to fill in a form with your personal details. Which detail is most dangerous to provide?", 
        "Your favorite color", 
        "Your date of birth", 
        "Your opinion about the product", 
        "Your monthly income", 
        "B"),
        
    (1, "You receive an email claiming to be from your bank, but the email starts with 'Dear Customer' instead of using your real name. It also contains spelling and grammar errors. What is the best conclusion?", 
        "It’s likely a harmless promotional email.", 
        "The bank might have changed how they greet customers.", 
        "It’s likely a phishing attempt, because official institutions usually use personal greetings and maintain correct spelling.", 
        "The email just got your name wrong by accident.", 
        "C"),
        
    (1, "You see an email offer claiming you won a free trip to a luxury resort. To claim, you must click a link and provide credit card details for 'verification.' This is likely:", 
        "A legitimate free giveaway", 
        "A routine promotional method", 
        "A phishing scam", 
        "A standard security procedure", 
        "C"),
        
    (1, "You receive an email with a hyperlink stating 'www.yourbank.com,' but when you hover over it, you notice the actual link leads to 'www.xyz-unknown-site.com.' Which statement is most accurate?", 
        "This is a normal redirect for a bank website.", 
        "This is a security measure used by real banks.", 
        "This is likely a phishing link, and you should not click it.", 
        "It’s a typo that won’t cause any harm.", 
        "C"),
        
    (1, "You get a call from someone saying they’re from a well-known tech support team. They claim your computer is infected and request remote access to fix it. What should you do?", 
        "Allow them remote access immediately to fix the issue.", 
        "Provide them your personal info (like date of birth) as proof of identity.", 
        "Politely hang up and call the official support line if you actually need help.", 
        "Ask them to call again tomorrow to see if they are persistent.", 
        "C"),
        
    (1, "You click on a link in a message that claims it’s from your friend. It opens a login page for a popular social media site, but the URL looks different. How should you proceed?", 
        "Enter your username and password to see if it works.", 
        "Ask your friend why they sent the link and confirm it’s legit.", 
        "Bookmark the page in your browser for easier access.", 
        "Try different usernames and passwords to see if it’s real.", 
        "B"),
        
    (1, "You have an email from a colleague with an attachment labeled 'Important Document.' However, the colleague’s email address looks slightly altered (e.g., 'john.smith@companu.com' instead of 'john.smith@company.com'). What should you do?", 
        "Download and open the attachment right away.", 
        "Reply to that email asking why the address is spelled differently.", 
        "Call or text your colleague through a known method to confirm they sent it.", 
        "Forward the email to everyone in your contact list as a warning.", 
        "C"),
        
    (1, "Which of the following is the best way to protect yourself from phishing attacks in general?", 
        "Using the same strong password for every account.", 
        "Turning off your antivirus software to speed up your computer.", 
        "Being cautious with suspicious emails and links, enabling security features like multi-factor authentication (MFA), and keeping software up to date.", 
        "Only trusting emails that come late at night, as scammers avoid those hours.", 
        "C"),
        
    # Stage 02 - Password Strength
    (2, "You have multiple online accounts (social media, email, online shopping). You use the same password across all of them for convenience. Which statement best describes why this might be risky?", 
        "It’s not risky; it’s a smart time-saver.", 
        "If one account is hacked, the hacker could access all your other accounts.", 
        "You only need to update one password occasionally.", 
        "Websites prefer you to have the same password for simplicity.", 
        "B"),
        
    (2, "Which of the following characteristics usually makes a password stronger?", 
        "Short and easy to remember, such as '12345'", 
        "Contains common words like 'password' or 'qwerty'", 
        "A mix of upper- and lower-case letters, numbers, and special symbols", 
        "Personal details like your birthday or pet’s name", 
        "C"),
        
    (2, "Between length and complexity, which factor most significantly increases password strength?", 
        "Only complexity matters—special symbols are enough.", 
        "Short but complex passwords are always best.", 
        "Length is more important; a longer password or passphrase is usually harder to crack.", 
        "Neither length nor complexity matters—only using an app to generate passwords is important.", 
        "C"),
        
    (2, "Your friend suggests creating a password like 'PurpleSunset_1234!' instead of 'Psun1234.' How is this beneficial?", 
        "It looks pretty and more stylish.", 
        "It’s a bit longer, has mixed characters, and is easier to remember compared to random characters.", 
        "It’s the same strength as any other password.", 
        "Random letters alone are always stronger than words.", 
        "B"),
        
    (2, "You haven’t changed your main email password in over 3 years. Which is the best reason to consider updating it?", 
        "It’s a trend to change passwords regularly, so you should follow it.", 
        "Attackers may have cracked your password if it’s been circulating in a data breach without your knowledge.", 
        "You get bored seeing the same password.", 
        "Changing passwords too often can weaken security.", 
        "B"),
        
    (2, "You’re at a café and use a public computer to check your social media. The website asks if you’d like to stay logged in (e.g., 'Remember Me'). What should you do?", 
        "Click 'Remember Me' for convenience.", 
        "Use 'Remember Me' and hope no one else checks that computer.", 
        "Never click 'Remember Me' or save passwords on a public device, and log out after you’re done.", 
        "It doesn’t matter because it’s just social media.", 
        "C"),
        
    (2, "What’s the safest way to store multiple complex passwords if you struggle to remember them?", 
        "Write them on a sticky note and keep it on your desk.", 
        "Use one short, simple password that’s easy to memorize for all accounts.", 
        "Store them in an encrypted password manager.", 
        "Ask a close friend to remember them for you.", 
        "C"),
        
    (2, "Why is a password like 'Jack1990' or 'Jane_Dubai' risky?", 
        "Because using your personal info (e.g., name, birth year, city) makes passwords easy for attackers to guess or find.", 
        "It’s actually strong since it has uppercase letters and numbers.", 
        "Friends can’t guess it.", 
        "It’s only risky if you share it with strangers.", 
        "A"),
        
    (2, "You get an email saying 'Your Netflix password is about to expire, click here to reset,' but you didn’t request a reset. What should you do?", 
        "Click the link and reset your password just in case.", 
        "Reply with your current password so they can verify you.", 
        "Ignore it or log in to Netflix directly (not via the email) to confirm if there’s an official notice.", 
        "Immediately close your Netflix account.", 
        "C"),
        
    (2, "Which of the following best describes why enabling multi-factor authentication (MFA) strengthens your password security?", 
        "It doesn’t; MFA only slows down your login process.", 
        "With MFA, you can use a weaker password because you have a second factor.", 
        "MFA adds an extra layer (like a one-time code or fingerprint) making it harder for attackers to access your account even if they guess your password.", 
        "MFA automatically changes your password each week without your knowledge.", 
        "C"),
        
    # Stage 03 - Vulnerability Detection
    (3, "In cybersecurity, a 'vulnerability' is best described as:", 
        "A hidden software feature that speeds up your computer.", 
        "An intentional backdoor created by developers for easy access.", 
        "A weakness in a system or software that attackers can exploit.", 
        "A random bug that never affects security.", 
        "C"),
        
    (3, "Which daily-life scenario best illustrates a 'vulnerability'?", 
        "Leaving your car locked and keys hidden.", 
        "Sharing your house key with a stranger you just met.", 
        "Having a strong, unique password for each website.", 
        "Installing antivirus software on your computer.", 
        "B"),
        
    (3, "Why do phone and computer apps frequently prompt you to install updates?", 
        "They want to slow down your device so you’ll buy a new one.", 
        "They only update the app’s icon and color theme.", 
        "They’re fixing security flaws and improving performance, often addressing known vulnerabilities.", 
        "They do it to fill up your storage space.", 
        "C"),
        
    (3, "Using free, public Wi-Fi in a café without any security measures can be considered a vulnerability because:", 
        "Public networks are always safe.", 
        "You can never browse social media over public Wi-Fi.", 
        "Attackers on the same network can potentially intercept unencrypted data.", 
        "It has nothing to do with security if your phone is fully charged.", 
        "C"),
        
    (3, "Installing and regularly updating an antivirus (or anti-malware) tool helps in vulnerability detection by:", 
        "Slowing down your computer intentionally.", 
        "Searching for and removing known malicious software that exploits vulnerabilities.", 
        "Preventing you from installing any app at all.", 
        "Making your device immune to physical damage.", 
        "B"),
        
    (3, "Which of these represents a likely vulnerability in everyday life?", 
        "Using unique, complex passwords for each account.", 
        "Keeping your phone locked with a PIN or fingerprint.", 
        "Sharing your email password with a friend so they can 'check messages' for you.", 
        "Using multi-factor authentication.", 
        "C"),
        
    (3, "Having an old operating system on your computer or phone can be risky because:", 
        "Older devices are always superior in performance.", 
        "They cannot run any apps at all.", 
        "Hackers already know about unpatched vulnerabilities in old systems.", 
        "You can’t watch videos on them.", 
        "C"),
        
    (3, "Which of the following is a simple way to detect or avoid vulnerabilities at home?", 
        "Never change your default router password because it’s 'official.'", 
        "Install software from unknown websites if it’s free.", 
        "Regularly check for software updates and use only trusted download sources.", 
        "Disable your firewall to speed up internet.", 
        "C"),
        
    (3, "A phone call claiming to be from 'tech support' asks for your computer password. This is a vulnerability because:", 
        "They’re always legitimate companies helping you for free.", 
        "If you give them your password, they can access and exploit your system.", 
        "Everyone gives out passwords on the phone.", 
        "Passwords are meant to be shared with support staff.", 
        "B"),
        
    (3, "Why can smart devices (e.g., smart TV, smart doorbell) become vulnerabilities?", 
        "They never receive software updates.", 
        "Hackers can use unpatched flaws in these devices to gain access to your home network.", 
        "They are immune to any hacking attempts.", 
        "They only affect your electricity bill, not security.", 
        "B"),
        
    # Stage 04 - Incident Response
    (4, "In the context of cybersecurity, which of the following would most likely be considered a security 'incident'?", 
        "Finding a new music app on your phone’s app store.", 
        "Spilling water on your laptop keyboard.", 
        "Noticing unauthorized charges on your credit card statement.", 
        "Charging your phone overnight while you sleep.", 
        "C"),
        
    (4, "You suspect your social media account has been hacked because suspicious posts are appearing. What should you do first?", 
        "Publicly announce the hack on your profile.", 
        "Immediately change your password and enable additional security (like two-factor authentication).", 
        "Stop using social media altogether.", 
        "Keep posting and hope the hacker stops.", 
        "B"),
        
    (4, "You receive an unexpected email claiming you’ve won a prize, and it asks for personal information. How do you respond as part of a basic 'incident response'?", 
        "Reply with partial information, just in case it’s real.", 
        "Click any links to see if the email is genuine.", 
        "Do not click, do not reply. Verify with the official website or ignore.", 
        "Share the email on social media to warn everyone about your winnings.", 
        "C"),
        
    (4, "You notice a coworker left a work laptop unlocked in a public café. As part of your workplace’s incident response, what’s the recommended action?", 
        "Quietly lock it yourself and say nothing.", 
        "Tell the coworker you’ll report them to the police.", 
        "Immediately notify the appropriate security or IT person about the potential security risk.", 
        "Take the laptop home for safekeeping.", 
        "C"),
        
    (4, "Your friend’s personal website got hacked, and malicious pop-ups are now displayed. Which best describes the containment phase in incident response?", 
        "Deleting the website entirely.", 
        "Disconnecting or taking the site offline temporarily to stop further damage.", 
        "Asking visitors to ignore the pop-ups.", 
        "Using social media to blame the hosting company.", 
        "B"),
        
    # Stage 05 - Cyber Puzzles
    (5, "You receive an urgent email from your 'CEO' asking you to transfer money immediately to a new vendor. The email address looks slightly off, and the tone is unusual. You suspect it might be a scam. What’s the best way to confirm it’s genuine?", 
        "Email back asking if it’s really them.", 
        "Transfer the money quickly, just in case.", 
        "Call your CEO or use a known internal company phone number to verify the request.", 
        "Forward the email to all your coworkers to see if they think it’s real.", 
        "C"),
        
    (5, "You get a text message that says you’ve won a free smartphone. It includes a link to 'claim your prize.' You never entered any contest. What should you do?", 
        "Click the link right away because a free phone is too good to miss.", 
        "Ignore or delete the text without clicking, and if curious, confirm the contest from the legitimate company’s official site.", 
        "Share the link on social media so others can 'win' too.", 
        "Ask your friends to click it first to see if they also win.", 
        "B"),
        
    (5, "You find a random USB drive on a desk at the library labeled 'TOP SECRET.' What’s the safest step if you’re curious about its contents?", 
        "Plug it into your work or personal computer immediately to see what’s inside.", 
        "Use a friend’s computer so it won’t affect yours.", 
        "Give it to a library staff member or an authority figure (e.g., campus security), or simply leave it.", 
        "Plug it into your TV’s USB port at home.", 
        "C"),
        
    (5, "While browsing, you see a pop-up saying your computer is infected. It claims you must 'click here' to clean your system. How do you respond?", 
        "Immediately click the pop-up to download the recommended tool.", 
        "Restart your computer and hope the problem goes away.", 
        "Close the pop-up and run a trusted antivirus or anti-malware scan.", 
        "Ignore it and continue browsing.", 
        "C"),
        
    (5, "You’re entering your ATM PIN at the supermarket checkout, and you notice someone behind you trying to watch the keypad. What’s the best puzzle solution here?", 
        "Let them see because it’s just your PIN, and you can change it later.", 
        "Use one hand or your wallet to shield the keypad while typing.", 
        "Ask them nicely to look away.", 
        "Stop entering your PIN and simply pay later.", 
        "B"),
        
    (5, "You get an email from 'ShieldMyPC' claiming your antivirus is about to expire. However, you don’t recall ever installing 'ShieldMyPC.' They want you to click a link to renew. How do you handle it?", 
        "Click the link just to see the expiration details.", 
        "Forward it to your friends to see if they got the same email.", 
        "Do nothing or delete the email, then check your actual antivirus software or subscriptions.", 
        "Reply with your credit card details, because maybe you forgot you installed it.", 
        "C"),
        
    (5, "While online shopping, you see a brand-new gaming console being sold for 90% off by an unknown seller. The site looks a bit sketchy. Which is the safest approach?", 
        "Buy it immediately before the offer ends.", 
        "Ask your friends if they trust the site, then decide.", 
        "Stick to reputable sellers or official channels; if the deal seems too good to be true, it likely is.", 
        "Share the link with everyone and ask them to test-purchase.", 
        "C"),
        
    (5, "You get a notification saying, 'Your account was logged in from a new location' at 3 AM, but you were asleep. What’s your best next step?", 
        "Ignore it since it might be a random glitch.", 
        "Immediately change your password and enable two-factor authentication if not already on.", 
        "Sign out of all devices next week.", 
        "Send your password to support to confirm you are the owner.", 
        "B"),
        
    (5, "A social media post says, 'Find out your superhero name! Use your birth month, your pet’s name, and the last four digits of your phone number!' People are sharing their results. Is it safe to join in?", 
        "Yes, it’s just fun. Everyone is doing it.", 
        "It’s safe as long as you only share your phone number and keep your pet’s name secret.", 
        "No, it could reveal personal information that scammers can use (birth month, phone digits, pet name often used as passwords/security questions).", 
        "Share only with your private group of friends.", 
        "C"),
        
    (5, "You’re traveling and need to access your bank account. The airport only has free public Wi-Fi with no password. What’s the safest approach?", 
        "Log in to your bank anyway—free Wi-Fi is a bonus.", 
        "Wait until you have a secure network, or use your mobile data or a VPN for a more secure connection.", 
        "Ask the airport staff for any login instructions, then do your banking.", 
        "Connect using the free Wi-Fi but quickly log out after.", 
        "B")
]

# Insert New Sample Questions
cursor.executemany('''
INSERT INTO Questions (Stage, QuestionText, OptionA, OptionB, OptionC, OptionD, CorrectAnswer)
VALUES (?, ?, ?, ?, ?, ?, ?)
''', sample_questions)

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database, tables, and new sample questions have been successfully created!")

