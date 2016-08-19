
# Please use Python 3.0+

from bs4 import BeautifulSoup
import bs4
import requests

class User_info:
    'A class for user'
 
    def __init__( self, username='',introdution='',  website = '',
                        followers=0, last_hour=0, today=0, yesterday=0, media=0):
        
        self.username = username
        self.introdution = introdution
        self.website = website
        
        self.followers = followers
        self.last_hour = last_hour
        self.today = today
        self.yesterday = yesterday
        self.media = media
        
    def displayUser(self):
        print ("Name: %s \n Introduction: %s \n Website: %s \n Followers: %10d \tLast Hour: %8d \tToday: %8d \tYesterday: %8d \tMedia: %8d \n"% 
               (self.username, self.introdution, self.website, self.followers, self.last_hour, self.today, self.yesterday, self.media)) 
    

        
def main():
    
    users = []
    numbers =[] 
    introductions=[]
    websites = []
    
    for i in range(1,3):   # max = 87  Maximun 87 pages
        r  = requests.get("http://zymanga.com/millionplus/"+str(i)+"f")
        data = r.text
        soup = BeautifulSoup(data, 'html.parser')
    
        # ----- Get usernames -----  
        
        for username in soup.find_all('span', id='username'):
            for a_tag in username.find_all('a'):
             
                new_user = User_info(str(a_tag.text) )
                users.append( new_user ) 

        # ----- Get introdutions and websites-----    
       
        tags_of_introductions = soup.find_all('td', style="width: 500px; vertical-align: top; word-wrap: break-word")

        for tag in tags_of_introductions:
            res = tag.find('span',id="website")     # find website links
            if(res):
                websites.append(str(res.text))
            else:
                websites.append('N/A')
       
            if len(tag.contents) > 0:       # find personal introductions
                if isinstance(tag.contents[0], bs4.NavigableString):
                    introductions.append(str(tag.contents[0].encode('utf-8').strip()))
                else:
                    introductions.append("N/A")
            else:
                introductions.append("N/A")
                
      
        # ----- Get numbers of followers, last_hour, today, yesterday, media -----
        
        tags_of_numbers =  soup.find_all('td',style="width: 100px; text-align: center")
        for tag in tags_of_numbers:
            numbers.append( int( str(tag.find('br').next_sibling).replace(',', '')) )   # string to int number
        
        
        print ("\n Total Users %d\n" % len(users))
        
        
        # ----- Assign to objects -----
        
        for i in range(0, len(numbers), 5):
            j = i/5
            users[j].followers = numbers[i]
            users[j].last_hour = numbers[i+1]
            users[j].today = numbers[i+2]
            users[j].yesterday = numbers[i+3]
            users[j].media = numbers[i+4]
            
            users[j].website = websites[j]
            users[j].introdution = introductions[j]
        
        # ----- display -----
        for u in users:
            u.displayUser()
        
if __name__ == '__main__':
    main()

        
