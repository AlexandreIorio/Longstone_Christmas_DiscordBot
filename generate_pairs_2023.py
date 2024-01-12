"""Generate user ---gifts to---> another user pairs"""
import random

# whom a user could gift to
# exclude: itself, partner and people they gifted to in the past two years
# the rule about forbidden reciprocal gifts does not apply
def could_gift_to(user, users, couple_dict, penultimate_christmas_dict, last_christmas_dict):
    candidates = users[:]

    # rule: not self
    candidates.remove(user)

    # rule: not partner
    if user in couple_dict:
        candidates.remove(couple_dict[user])

    # rule: not gifted in past two years
    # check user was there for the gift-giving of that year
    # and check the person the user gave to in 2021 is also still here this year
    if user in penultimate_christmas_dict and penultimate_christmas_dict[user] in users:
        candidates.remove(penultimate_christmas_dict[user])
    if user in last_christmas_dict and last_christmas_dict[user] in users:
        candidates.remove(last_christmas_dict[user])
    
    return candidates


def create_pairing(users, couple_dict, penultimate_christmas_dict, last_christmas_dict):
    def pair_users(paired, users_candidates):
        """ generate a user:user-to-gift-to pairing 

        dynamic programming
        DFS search
        the args combined (paired, users_candidates) represent a state
        Args:
            paired: users with matching recipient already assigned
                looks like [(user1, target1), ...]
            users_candidates: users yet to have recipient assigned (with their candidates)
                looks like [(user1, [candidate1, candidate2]), ...]
    

        Returns:
            A pairing [(user1, match1),...]. None if no solution
        """

        # finished
        if not users_candidates:
            return paired
        
        [(user, candidates), *remaining_users_candidates] = users_candidates

        if not candidates:
            # zero candidates : unsolvable!
            return None

        for candidate in candidates:
            # print(user, "gifts to", candidate)

            # rule: no reciprocal gift (x to y means no y to x)
            # since 'user' gifts to 'candidate' => 'candidate' cannot gift to 'user'
            remaining_users_candidates_new = [(person, candidates) if person != candidate else (person, [c for c in candidates if c != user]) for (person, candidates) in remaining_users_candidates]

            # candidate will receive a gift from user
            # no other user can gift to candidate
            remaining_users_candidates_new = [(person, [c for c in candidates if c != candidate]) for (person, candidates) in remaining_users_candidates_new]

            new_state = (paired + [(user, candidate)], remaining_users_candidates_new)
            result = pair_users(*new_state)
            if result : return result
        return None

    users_candidates = [(user, could_gift_to(
        user, 
        users, 
        couple_dict, 
        penultimate_christmas_dict, 
        last_christmas_dict)) for user in users]

    # shuffle to create different result each time
    for (user, candidates) in users_candidates:
        random.shuffle(candidates)

    state = ([], users_candidates)
    return pair_users(*state)
