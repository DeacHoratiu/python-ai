#ce e un string? # de ce il folosim? ce e in spate?


var1 = "a"
var2="007"
var3='asd'

arr1=[10,20,30]


msg = "LLM Agents are agents usually process strings as tokens. it tokenizes them."

print("token" in msg)
print(msg.find("tok"))

#string is imutable

print(msg.lower())
print(msg)

#split a string by separator
split_string = msg.split(" ")
print(split_string)
print("-".join(split_string))
#numaram substringuri
c = msg.lower().count("agents")
print(c)

with open("lesson_05_json_data.py", "r") as f:
    content = "".join(f.readlines())
    print(content)
    print(f"File has {len(content)} characters")
    print(f"json shows up {content.lower().count("json")} times in our file")

# streaming
# f.readline()