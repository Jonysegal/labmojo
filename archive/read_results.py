num = 0
with open("results/results-clean.json", 'r+') as file:
  data = json.load(file)
  for pi in data['data']:
      num+=1
    print(pi)


def save_file(pi, file_name):
    m = open(file_name,'a')  # Amend mode
    json.dump(pi, m)  # Write JSON
    m.write(',')  # Add comma
    m.close()  # Close the file
    return


f = open("results/results.json")
data = f.read()
start = data[:-4]
end = "]}"

m = open('results/results-clean.json','w')  # Amend mode
m.write(start+end)
m.close()

nn = open('results/results-clean.json')
data = nn.read()
data[-10:]
