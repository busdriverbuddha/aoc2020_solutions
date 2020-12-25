#!/usr/bin/env python
# coding: utf-8

# In[25]:


card, door = map(int, open("input").readlines())

v = 1
loopsize = 0
while True:
    loopsize += 1
    v *= 7
    v %= 20201227
    if v == card:
        subject_number = door
        break
    elif v == door:
        subject_number = card
        break

v = 1
for _ in range(loopsize):
    v *= subject_number
    v %= 20201227

print(v)


# In[ ]:




