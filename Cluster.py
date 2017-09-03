def KNN(group_means, trainer):
	num_groups = len(group_means)
	#trainer = [30,21,26,28,40,35,27,32,45,36]
	#trainer = [9,1,2,10,14,10,6,9,17,7]
	trainer.sort()
	per_group = len(trainer)*1.0/num_groups
	group_members = [0] * num_groups
	group_member_count = [0] * num_groups
	group_pointer_position = [0] * num_groups
	assigned_groups = {}

	t = 0
	c = per_group
	i = 0
	while t < len(trainer):
		this_group = int(c-t)
		s = 0
		group_members[i] = []
		for j in range(this_group):
			s += trainer[t+j]
			group_members[i].append(trainer[t+j])
			assigned_groups[trainer[t+j]] = i
			group_member_count[i] += 1
		group_means[i] = s*1.0/this_group
	
		t += this_group
		c += per_group	
		group_pointer_position[i] = t
		i += 1
	
	changed = True
	while changed:
		changed = False
		for i in range(num_groups-1):
			if abs(trainer[group_pointer_position[i]-1]-group_means[i]) < abs(trainer[group_pointer_position[i]-1]-group_means[(i+1)]):
				if abs(trainer[group_pointer_position[i]]-group_means[i+1]) > abs(trainer[group_pointer_position[i]]-group_means[(i)]):
					if group_member_count[i+1] != 1:
						changed = True	
						# Move pointer forward	
						group_means[i] = (group_means[i]*group_member_count[i] + trainer[group_pointer_position[i]])/(group_member_count[i]+1)
						group_means[i+1] = (group_means[i+1]*group_member_count[i+1] - trainer[group_pointer_position[i]])/(group_member_count[i+1]-1)
						group_members[i+1].remove(trainer[group_pointer_position[i]])
						group_members[i].append(trainer[group_pointer_position[i]])
						group_member_count[i] += 1
						group_member_count[i+1] -= 1
						group_pointer_position[i] += 1
						assigned_groups[trainer[group_pointer_position[i]]] = i
						break				
			else:
				if group_member_count[i] != 1:
					changed = True
					# Move pointer backward
					group_means[i] = (group_means[i]*group_member_count[i] - trainer[group_pointer_position[i]-1])/(group_member_count[i]-1)
					group_means[i+1] = (group_means[i+1]*group_member_count[i+1] + trainer[group_pointer_position[i]-1])/(group_member_count[i+1]+1)
					group_members[i].remove(trainer[group_pointer_position[i]-1])
					group_members[i+1].append(trainer[group_pointer_position[i]-1])
					group_member_count[i] -= 1
					group_member_count[i+1] += 1
					group_pointer_position[i] -= 1
					assigned_groups[trainer[group_pointer_position[i]]] = i+1
					break	
	return group_means, assigned_groups
