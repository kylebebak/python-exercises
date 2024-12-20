class DecisionNode(object):

	def __init__(self, kind = "decision", condition = None, val = None, children = None):
		self.kind = kind
		self.condition = condition or [0, " < 0"]
		self.val = val
		self.children = children or [None, None]


	def evaluate(self, point):
		if self.kind == "prediction":
			return self.val


		if eval(str(point[self.condition[0]]) + self.condition[1]):
			return self.children[0].evaluate(point)
		else:
			return self.children[1].evaluate(point)



	# i like the look of this more when implemented with iteration than with recursion
	def insert(self, decision_node, node_traversal = None):

		if node_traversal is None:
			node_traversal = [0]

		parent = self
		for node in node_traversal[:-1]:
			parent = parent.children[node]

		parent.children[node_traversal[-1]] = decision_node



	def insert_recursive(self, decision_node, node_traversal = None):

		if node_traversal is None:
			node_traversal = [0]

		if len(node_traversal) == 1:
			self.children[node_traversal[0]] = decision_node

		else:
			self.children[node_traversal[0]].insert(decision_node, node_traversal[1:])






root = DecisionNode(condition = [0, " < 45"])

root.insert(DecisionNode(condition = [1, " < 110"]), [0])
root.insert(DecisionNode(condition = [1, " < 75"]), [1])

root.insert(DecisionNode(kind = "prediction", val = "doesn't buy"), [0, 0])
root.insert(DecisionNode(kind = "prediction", val = "buys"), [0, 1])
root.insert(DecisionNode(kind = "prediction", val = "doesn't buy"), [1, 0])
root.insert(DecisionNode(kind = "prediction", val = "buys"), [1, 1])

print root.condition
print root.children[0].condition
print root.children[1].condition
print root.children[0].children[0].val
print root.children[0].children[1].val
print root.children[1].children[0].val
print root.children[1].children[1].val



print
print

print "BUY"
print (28,145), root.evaluate((28,145))
print (38,115), root.evaluate((38,115))
print (43,83), root.evaluate((43,83))
print (50,130), root.evaluate((50,130))
print (50,90), root.evaluate((50,90))
print (50,60), root.evaluate((50,60))
print (50,30), root.evaluate((50,30))
print (55,118), root.evaluate((55,118))
print (63,88), root.evaluate((63,88))
print (65,140), root.evaluate((65,140))

print
print "DOESN'T BUY"
print (23,40), root.evaluate((23,40))
print (25,125), root.evaluate((25,125))
print (29,97), root.evaluate((29,97))
print (33,22), root.evaluate((33,22))
print (35,63), root.evaluate((35,63))
print (42,57), root.evaluate((42,57))
print (44, 105), root.evaluate((44, 105))
print (55,63), root.evaluate((55,63))
print (55,20), root.evaluate((55,20))
print (64,37), root.evaluate((64,37))




