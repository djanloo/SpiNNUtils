from abstract_grandparent import AbstractGrandParent
from abstract_has_label import AbstractHasLabel
from abstract_has_constraints import AbstractHasConstraints

from spinn_utilities.overrides import overrides


class GrandParent(AbstractGrandParent):

    def label(self):
        return "GRANDPARENT"

    def set_label(selfself, label):
        pass

    @overrides(AbstractHasConstraints.add_constraint)
    def add_constraint(self, constraint):
        raise Exception("We set our own constrainst")

    @overrides(AbstractHasConstraints.constraints)
    def constraints(self):
        return ["No night feeds", "No nappy changes"]


