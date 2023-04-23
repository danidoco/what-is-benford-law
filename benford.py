from collections import Counter
import re
import sys
import requests
from bs4 import BeautifulSoup
from colorama import init, Fore, Back, Style
from matplotlib import pyplot as plt

def crawl_text(url: str) -> str:
   response = requests.get(url)
   html = response.text

   soup = BeautifulSoup(markup=html, features="html.parser")
   text = soup.get_text(separator="\n", strip=True)

   return text


def extract_numbers(string: str) -> list[int]:
   numbers = re.findall(r"\d+", string)
   return [int(number) for number in numbers if int(number) != 0]

def get_first_digit_percentage(numbers: list[int]) -> dict[int, int]:
   numbers = sorted(numbers)

   # get first digit count
   first_digit = [int(str(number)[0]) for number in numbers]
   first_digit_count = dict(Counter(first_digit))

   # get first digit percentage
   first_digit_percentage = {}

   total_count = sum(first_digit_count.values())

   for first_digit, count in first_digit_count.items():
      percentage = (count / total_count) * 100
      first_digit_percentage[first_digit] = percentage

   return first_digit_percentage

def plot_figure(data_dict) -> None:
   x_data = data_dict.keys()
   y_data = data_dict.values()

   plt.clf()
   
   # draw histogram
   plt.bar(x_data, y_data, color="#009")

   for rect in plt.gca().patches:
      plt.gca().text(rect.get_x() + rect.get_width()/2, rect.get_height(), 
                     round(rect.get_height(), 1), ha='center', va='bottom')

   # draw line graph
   plt.plot(x_data, y_data, linestyle="-", marker="", color="#4472C4")

   # set xlabel and ticks
   plt.xlabel("First Digit")
   plt.xticks(list(x_data))

   # set ylabel and ticks
   plt.ylabel("Percentage (%)")

   # set figure title
   plt.title("Benford's Law")

   plt.show()

if __name__ == "__main__":
   init(convert=True)

   urls_path = sys.argv[1]

   print(Fore.GREEN + "* " + Fore.RESET + f"Collecting urls from {urls_path}")

   with open(urls_path, "r") as f:
      urls = [url.strip() for url in f]

   numbers = []

   for i, url in enumerate(urls):
      print(f"{i + 1}. " + Fore.CYAN + url + Fore.RESET)
      
      text = crawl_text(url)
      extracted_numbers = extract_numbers(text)
      
      numbers.extend(extracted_numbers)

   first_digit_percentage = get_first_digit_percentage(numbers)

   print(Fore.GREEN + "* " + Fore.RESET + "Plotting figure")
   plot_figure(first_digit_percentage)
   print(Fore.GREEN + "* " + Fore.RESET + "Done")
   