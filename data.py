# this is a test....


chicken = {
  "calories": 250,
  "category": "protein",
  "model": "Mustang",
  "year": 1964
}
cake = {
  "calories": 1000,
  "category": "carb",
  "model": "Mustang",
  "year": 1964
}

print(chicken["calories"] + cake["calories"] )

meal = []

meal.append(chicken["category"])
meal.append(chicken["category"])
meal.append(chicken["category"])
meal.append(chicken["category"])
meal.append(cake["category"])

print(meal)

proteins = 0

for i in meal:
    print(i)
    if i == "protein":
        proteins += 1

print(proteins)
