import numpy as np


def make_ordered_skel(skel_coords, skel_ends, head_pos):

    # sort all skel points
    # - idea is to start at one end of the worm and then find the next skeleton point that is nearest to that end,
    #   this point will be our new reference point, then we find the next point on the skeleton that is nearest
    #   to our new reference point and make that the reference, while we do that we save all coordinates and by that
    #   we get a sequence of coordinates that symbolizes the worm
    # - we want an ordered list of all points of the skeleton so we can place evenly spaced points

    ordered_skel = np.array([[0, 0]])  # make empty list where we will save all coordinates of the skeleton in order
    # print(ordered_skel.shape)
    # get new head pos from previous head pos
    end_distances = np.array(
        list(map(lambda x: np.sqrt((x[0] - head_pos[0]) ** 2 + (x[1] - head_pos[1]) ** 2), skel_ends)))
    ind = np.argsort(end_distances)
    skel_ends = [skel_ends[i] for i in ind]
    head_pos = skel_ends[0]
    reference = head_pos

    # order the skel coords in an ordered skel
    while np.size(skel_coords) != 0:  # we loop until all coordinates have been used
        # make an array of all distances to the reference point
        distances_arr = np.array(
            list(map(lambda x: np.sqrt((x[0] - reference[0]) ** 2 + (x[1] - reference[1]) ** 2), skel_coords)))
        ind = np.argsort(distances_arr)  # argsort the distances...
        skel_coords = [skel_coords[i] for i in ind]  # ...and sort the coordinates by their distance to the ref
        reference = skel_coords[0]  # make new ref point the nearest point
        ref = np.array([reference])
        # print(ref.shape)
        # print(np.size(skel_coords))
        # print(ref)
        ordered_skel = np.concatenate((ordered_skel, ref))  # add new point to the sorted list of coordinates
        skel_coords = skel_coords[1:]  # remove the added coordinate, so it doesn't get added again

    ordered_skel = ordered_skel[2:]  # remove the head that was added twice

    return ordered_skel, head_pos
