from django.core.management.base import BaseCommand
import json,requests,time
from bs4 import BeautifulSoup

class Command(BaseCommand):
            help= "Scrapes Hacker News and posts data to the backend"
            def add_arguments(self,parser):
                 parser.add_argument('--interval',type=int,default=600,help='Interval in seconds between scrapes')
            def handle(self, *args, **options):
                 interval = options['interval']
                 self.stdout.write(self.style.SUCCESS(f"Starting scraper with interval {interval}s"))

                 while(True):
                      try:
                           self.scrape()
                      except Exception as e:
                           self.stdout.write(self.style.ERROR(f"Error Scraping: {e}")) 
                      time.sleep(interval)  





            def scrape(self):
                URL= "https://news.ycombinator.com/news"
                page= requests.get(URL)

                soup = BeautifulSoup(page.content,"html.parser")
                main_target=soup.find(id="bigbox")
                table_story=main_target.find('table')
                rows=table_story.find_all("tr")

                story=[]

                for row in rows:
                    if "athing" in row.get("class",[]):
                        # Rank
                        rank=row.find("span",class_="rank")
                        rank=rank.text
                        #Title
                        titleline=row.find("span",class_="titleline")
                        #Title URL
                        titleurl=titleline.a['href']
                        #Title Text
                        titleline=titleline.a.text

                        subtext_row= row.find_next_sibling("tr")
                        # Score PTS
                        score=subtext_row.find("span",class_="score")
                        score=score.text if score else "0 points"

                        # AGE
                        age=subtext_row.find("span",class_="age")
                        age=age.find("a").text if age else "Unkown"
                        # Who Posted
                        posted_by=subtext_row.find("a")
                        posted_by=posted_by.text if posted_by else "Unkown"
                        
                        print("rank ",rank," titleline ",titleline," titleurl ",titleurl," score ",score," posted_by ",posted_by," age ",age," Scraped Page Link ",URL)
                        # Creating a dict to put the story
                        results={
                            "Rank":rank,
                            "Title":titleline,
                            "Link_To_Article":titleurl,
                            "Points":score,
                            "Author":posted_by,
                            "Post_Time":age,
                            "Scraped_Page_Link":URL,
                        }
                        # appending the story to json response
                        story.append(results)
                json_response=json.dumps(story,indent=4)
                print(json_response)
                target_url="http://127.0.0.1:8000/BackendAPI/RecieveNews/"

                try:
                    response= requests.post(target_url,json=story)
                    response.raise_for_status()

                    if response.status_code in [200, 201]:
                        print("JSON data sent successfully!")
                        print("Response from server:",response.json())
                    else:
                        print(f"Failed to send Data. Status Code: {response.status_code}")
                        print("Response Content: ",response.text)
                except requests.exceptions.RequestException as e:
                    print("Error sending data: ",e)