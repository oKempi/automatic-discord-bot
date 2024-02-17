import asyncio
import csv
import psycopg2 as sql

FILE = "discord\\bot\\database\\infractions.csv"
csvR = csv.DictReader(FILE)
connection = sql.connect(
    host="109.81.95.40",
    port="5432",
    database="postgres",
    user="postgres",
    password="heslo1234")
cursor = connection.cursor()

class functions:
    def exc(prompt: str):
        cursor.execute(prompt)

    def find(user):
        for row in csvR:
            if row["name"] == user:
                return row["infractions"]

class infraction:
    def addPoint(self, user, amount):
            with open(FILE, "r") as file:
                csv_reader = csv.DictReader(file)
                data = list(csv_reader)

            userI = [row["name"] for row in data]
            infractions = [int(row["infractions"]) for row in data]

            if user not in userI:
                with open(FILE, "a", newline='') as write_file:
                    fieldnames = ["name", "infractions"]
                    csv_writer = csv.DictWriter(write_file, fieldnames=fieldnames)

                    csv_writer.writerow({"name": user, "infractions": amount})
                    print("\033[31m!\033[0m", f"Added {user} to infraction database")
            elif user in userI:
                to_find = self.find(user=user)
                if to_find <= 4:
                    print("\033[31m!\033[0m", f"{user} should be banned!")
                else:
                    index = userI.index(user)
                    infractions[index] += amount

                    with open(FILE, "w", newline='') as write_file:
                        fieldnames = ["name", "infractions"]
                        csv_writer = csv.DictWriter(write_file, fieldnames=fieldnames)

                        csv_writer.writeheader()
                        for u, infraction_count in zip(userI, infractions + 1):
                            csv_writer.writerow({"name": u, "infractions": infraction_count})
                    print("\033[31m!\033[0m", f"Added {amount} infraction(s) to {user}")
            return infraction_count

    async def subPoint(self, user):
        pass

    async def list(ctx):
        with open("discord\\bot\\database\\infractions.csv", "r") as logR:
            csvReader = csv.DictReader(logR)
            data = list(csvReader)
            col1_values = [row["name"] for row in data]
            col2_values = [row["infractions"] for row in data]
            await ctx.send(col1_values)
            await ctx.send(col2_values)
            print("\033[33m!\033[0m", "Infractions sent!")