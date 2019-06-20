#Taken from 112 website
def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)
filename = inspect.getframeinfo(inspect.currentframe()).filename
filePath = os.path.dirname(os.path.abspath(filename)) + "/TeamFiles/"

def dictAverage(dict):
    sum = 0
    count = 0
    for element in dict:
        if isinstance(dict[element], float):
            sum += dict[element]
            count += 1
    return sum / count
            

guard = {"height":[5, 3], "weight":177, "speed":0.75, "strength":0.7, "passing":0.8, "ballHandling":0.8,
         "shotForm":0.7, "accuracyLong":0.65, "accuracyMid":0.7, "accuracyShort":0.8, "steal":0.75,
         "block":0.7, "rebounding":0.7, "jump":0.9, "firstName":"Mike", "lastName":"Conley"}
forward = {"height":[5, 5], "weight":180, "speed":0.6, "strength":0.65, "passing":0.65, "ballHandling":0.7,
         "shotForm":0.9, "accuracyLong":0.8, "accuracyMid":0.85, "accuracyShort":0.95, "steal":0.7,
         "block":0.7, "rebounding":0.65, "jump":0.7, "firstName":"Kyle", "lastName":"Korver"}
center = {"height":[5, 10], "weight":209, "speed":0.8, "strength":0.75, "passing":0.7, "ballHandling":0.9,
         "shotForm":0.7, "accuracyLong":0.65, "accuracyMid":0.75, "accuracyShort":0.85, "steal":0.65,
         "block":0.6, "rebounding":0.7, "jump":0.8, "firstName":"Al", "lastName":"Horford"}
team = {"name":"DAK", "dColor": [127, 255, 0], "uColor": [0, 128, 0], "guard":guard,
        "forward":forward, "center":center}
team = str(team)
print("Team 1", dictAverage(guard), dictAverage(forward), dictAverage(center))


writeFile(filePath + "Team1.txt", team)
#Dakota Dragons-Offense

guard = {"height":[5, 0], "weight":155, "speed":0.8, "strength":0.65, "passing":0.75, "ballHandling":0.9,
         "shotForm":0.7, "accuracyLong":0.5, "accuracyMid":0.5, "accuracyShort":0.5, "steal":0.95,
         "block":0.6, "rebounding":0.7, "jump":0.8, "firstName":"Pat", "lastName":"Beverley"}
forward = {"height":[5, 7], "weight":183, "speed":0.75, "strength":0.8, "passing":0.7, "ballHandling":0.8,
         "shotForm":0.8, "accuracyLong":0.6, "accuracyMid":0.7, "accuracyShort":0.8, "steal":0.8,
         "block":0.75, "rebounding":0.85, "jump":0.7, "firstName":"TJ", "lastName":"Warren"}
center = {"height":[6, 2], "weight":240, "speed":0.6, "strength":0.9, "passing":0.65, "ballHandling":0.75,
         "shotForm":0.6, "accuracyLong":0.4, "accuracyMid":0.5, "accuracyShort":0.9, "steal":0.8,
         "block":0.9, "rebounding":0.95, "jump":0.7, "firstName":"Dwight", "lastName":"Howard"}
team = {"name":"HAW", "dColor": [255, 255, 0], "uColor": [184, 132, 11], "guard":guard,
        "forward":forward, "center":center}
team = str(team)
print("Team 2", dictAverage(guard), dictAverage(forward), dictAverage(center))

writeFile(filePath + "Team2.txt", team)
#Hawaii Supernova- Defense

guard = {"height":[5, 1], "weight":163, "speed":0.75, "strength":0.85, "passing":0.95, "ballHandling":0.8,
         "shotForm":0.6, "accuracyLong":0.55, "accuracyMid":0.9, "accuracyShort":0.8, "steal":0.8,
         "block":0.55, "rebounding":0.5, "jump":0.55, "firstName":"Chris", "lastName":"Paul"}
forward = {"height":[6, 0], "weight":215, "speed":0.7, "strength":0.8, "passing":0.8, "ballHandling":0.6,
         "shotForm":0.7, "accuracyLong":0.7, "accuracyMid":0.6, "accuracyShort":0.75, "steal":0.65,
         "block":0.8, "rebounding":0.9, "jump":0.75, "firstName":"Kevin", "lastName":"Love"}
center = {"height":[6, 1], "weight":227, "speed":0.65, "strength":0.8, "passing":0.85, "ballHandling":0.65,
         "shotForm":0.75, "accuracyLong":0.7, "accuracyMid":0.75, "accuracyShort":0.8, "steal":0.7,
         "block":0.8, "rebounding":0.8, "jump":0.7, "firstName":"Nikola", "lastName":"Jokic"}
team = {"name":"JER", "dColor": [0, 255, 255], "uColor": [0, 139, 139], "guard":guard,
        "forward":forward, "center":center}
team = str(team)
print("Team 3", dictAverage(guard), dictAverage(forward), dictAverage(center))

writeFile(filePath + "Team3.txt", team)
#Jersey Tide- Ball Movement

guard = {"height":[5, 2], "weight":170, "speed":0.9, "strength":0.75, "passing":0.8, "ballHandling":0.75,
         "shotForm":0.7, "accuracyLong":0.75, "accuracyMid":0.75, "accuracyShort":0.8, "steal":0.7,
         "block":0.5, "rebounding":0.6, "jump":0.65, "firstName":"Isaiah", "lastName":"Thomas"}
forward = {"height":[5, 9], "weight":197, "speed":0.75, "strength":0.7, "passing":0.6, "ballHandling":0.5,
         "shotForm":0.95, "accuracyLong":0.75, "accuracyMid":0.8, "accuracyShort":0.85, "steal":0.6,
         "block":0.6, "rebounding":0.75, "jump":0.7, "firstName":"Klay", "lastName":"Thompson"}
center = {"height":[6, 1], "weight":232, "speed":0.5, "strength":0.65, "passing":0.75, "ballHandling":0.5,
         "shotForm":0.7, "accuracyLong":0.75, "accuracyMid":0.8, "accuracyShort":0.9, "steal":0.55,
         "block":0.7, "rebounding":0.8, "jump":0.8, "firstName":"Boogie", "lastName":"Cousins"}
team = {"name":"VEG", "dColor": [240, 128, 128], "uColor": [220, 20, 60], "guard":guard,
        "forward":forward, "center":center}
team = str(team)
print("Team 4", dictAverage(guard), dictAverage(forward), dictAverage(center))

writeFile(filePath + "Team4.txt", team)
#Las Vegas Copperheads- Spacing