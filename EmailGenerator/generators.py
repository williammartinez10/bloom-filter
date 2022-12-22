import pandas as pd
import random
import string
import os


def check_gen():
    data = pd.read_csv("db_check.csv")
    df = pd.DataFrame(data)
    # Update sampling range accordingly if emails generated are < 10
    df.sample(n=random.randrange(5, 10)).to_csv('db_input.csv', mode='w', index=False, header=True)

    print('Done generating sample emails to check \n')

    
def email_gen(emails_to_generate = 20):
    alphabet = string.ascii_lowercase + string.digits

    def random_email(char_num):
        random_email = ''
        for x in range(char_num):
            random_email += ''.join(random.choice(alphabet))
        return random_email

    emails = ["@gmail.com", "@outlook.com", "@gmx.com", "@zoho.com", "@icloud.com", "@aol.com", "@proton.com", "@yahoo.com"]
    output = []

    for i in range(emails_to_generate):
        # Modify randint range to increase or decrease local email part
        output.append(random_email(random.randint(5, 10)) + random.choice(emails))

    dict = {'Email' : output}
    df = pd.DataFrame(dict)
    path = os.getcwd()
    df.to_csv(os.path.join(path,'db_check.csv'), mode='w', index=False, header=True)

    print('\nDone generating emails \n')