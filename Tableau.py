from itertools import permutations

class Tableau:
    def __init__(self, partition, notation="french"):
        self.shape = partition
        if type(self.shape) not in [list, tuple]:
            raise TypeError("Partition must be represented as a list or tuple.")

        self.notation = notation.lower()
        if self.notation not in ["french"]:
            raise ValueError("Notation must be 'french'. Only French notation is supported.")

        self.n = sum(partition)
        self.permutations = list(permutations(range(1, self.n + 1)))

        self.YT = self.get_yt()
        self.SIT = self.get_sit()
        self.SYCT = self.get_syct()

    def get_yt(self):
        """Generate all Young Tableaux (YT) for the given partition."""
        tableaux = []
        for perm in self.permutations:
            tableau = []
            start_idx = 0
            for row_length in reversed(self.shape):  # Construct rows from bottom to top
                end_idx = start_idx + row_length
                tableau.insert(0, list(perm[start_idx:end_idx]))  # Insert each row at the start
                start_idx = end_idx
            tableaux.append(tableau)
        return tableaux

    def is_sit(self, tableau):
        """Check if the tableau is a Standard Immaculate Tableau (SIT)."""
        # Check rows are strictly increasing (left-to-right)
        for row in tableau:
            if sorted(row) != row:
                return False

        # Check the leftmost column is strictly increasing (bottom-to-top)
        leftmost_col = [row[0] for row in tableau if len(row) > 0]  # Extract leftmost column
        if sorted(leftmost_col) != leftmost_col or len(set(leftmost_col)) != len(leftmost_col):
            return False

        return True


    def satisfies_triple_rule(self, tableau):
        """Check if the tableau satisfies the triple rule in French notation."""
        for i in range(len(tableau) - 1):  # Start from the second-to-last row
            current_row = tableau[i]
            for j, z in enumerate(current_row):
                if j == 0:
                    continue  # No left neighbor for z in this row

                # Check rows above for left neighbor x
                for k in range(i + 1, len(tableau)):  # Iterate through rows above
                    if j - 1 < len(tableau[k]):  # Ensure left neighbor exists in row k
                        x = tableau[k][j - 1]  # Left neighbor in row k
                        if x < z:
                            # Check the element to the right of x in the same row
                            if j < len(tableau[k]):  # If the right element exists
                                x_right = tableau[k][j]
                            else:  # If no element to the right, treat it as infinity
                                x_right = float('inf')

                            if not (x_right < z):  # Triple rule violation
                                return False
        return True


    def get_sit(self):
        """Generate all Standard Immaculate Tableaux (SIT) for the given partition."""
        tableaux = []
        for tableau in self.YT:
            if self.is_sit(tableau):
                tableaux.append(tableau)
        return tableaux

    def get_syct(self):
        """Generate all Standard Young Composition Tableaux (SYCT) for the given partition."""
        tableaux = []
        for tableau in self.SIT:
            if self.satisfies_triple_rule(tableau):
                tableaux.append(tableau)
        return tableaux
    
    def fundamental_map(self):
        if (len(self.shape) != 2):
            raise Exception("fundamental map can only be applied for partition of size (a+c,a)")
        if (self.shape[0] >= self.shape[1]):
            raise Exception("fundamental map can only be applied for partition of size (a,a+c) where c > 0")
        
        c = self.shape[1]-self.shape[0]

        for tableau in self.SIT:
            to_move = []
            for elem in tableau[1][::-1]:
                if ((elem - 1) not in tableau[0]) and (len(to_move) < c):
                    to_move.append(elem)

            tableau_new = []
            tableau_new.append(sorted(tableau[0]+to_move))
            tableau_new.append([x for x in tableau[1] if x not in to_move])

            # print(tableau)
            # print(tableau_new)
            self.print_transformation(tableau, tableau_new)
            print()




    def print_tableau(self, tableau):
        """Print a single tableau in French notation (rows bottom-to-top)."""
        for row in tableau[::-1]:  # Reverse rows for bottom-to-top display
            print(row)

    def print_transformation(self, tableau_1, tableau_2):

        tableau1 = tableau_1[::-1]
        tableau2 = tableau_2[::-1]

            # Get the maximum width of rows for consistent alignment
        max_width1 = max(len(" ".join(map(str, row))) for row in tableau1)
        max_width2 = max(len(" ".join(map(str, row))) for row in tableau2)

        # Zip rows from both tableaux and display them side by side
        for row1, row2 in zip(tableau1, tableau2):
            row1_str = " ".join(map(str, row1)).ljust(max_width1)
            row2_str = " ".join(map(str, row2)).ljust(max_width2)
            print(f"{row1_str}      {row2_str}")  # Add space between tableaux





if __name__ == "__main__":
    partition = [3,4] #enter partition size here
    tableau_obj = Tableau(partition)


    print(f"-- SIT of shape {partition} --")
    for sit in tableau_obj.SIT:
        tableau_obj.print_tableau(sit)
        print()

    print(f"-- SYCT of shape {partition} --")
    for syct in tableau_obj.SYCT:
        tableau_obj.print_tableau(syct)
        print()

    print(f"-- Transformation of {partition} --")
    tableau_obj.fundamental_map()