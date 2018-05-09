from shavtsak import Shavtsak, Soldier

adam = Soldier('Adam', 2)
sherman = Soldier('Sherman', 0)
gil = Soldier('Gil', 0)
karol = Soldier('Karol', 3)
hadar = Soldier('Hadar', 1)
mark = Soldier('Mark', 2)
shahar = Soldier('Shahar', 2)
noy = Soldier('Noy', 2)
yahli = Soldier('Yahli', 0)
luski = Soldier('Luski', 0)
shemer = Soldier('Shemer', 2)

soldiers = [adam, sherman, gil, karol, hadar, mark, shahar, noy, yahli, luski, shemer]

s = Shavtsak(soldiers)
s.assign([sherman], 'sunday', 'kitchen')
s.assign([hadar, gil], 'sunday', 'morning')
s.assign([luski, karol], 'sunday', 'evening')
s.assign([yahli, adam], 'sunday', 'night')

s.assign([luski], 'monday', 'kitchen')
s.assign([noy, sherman], 'monday', 'morning')
s.assign([hadar, shahar], 'monday', 'evening')
s.assign([yahli, sherman], 'monday', 'night')

s.assign([gil, hadar], 'tuesday', 'kitchen')
s.assign([karol, adam], 'tuesday', 'morning')
s.assign([shemer, noy], 'tuesday', 'evening')
s.assign([shahar, luski], 'tuesday', 'night')

s.assign(s.kitchen('wednesday', 2), 'wednesday', 'kitchen')
s.assign([adam, shemer], 'wednesday', 'morning')
s.assign([hadar, shahar], 'wednesday', 'evening')
s.assign([karol, adam], 'wednesday', 'night')

# s.assign(s.kitchen('thursday', 1), 'thursday', 'kitchen')
print(s)
