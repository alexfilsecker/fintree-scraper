from scraper.scrap import scrap

if __name__ == "__main__":
    movements = scrap("200719913", "46@8sA5uqV")
    for movement in movements:
        print(movement)
