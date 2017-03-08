from sphinxformat.SphinxClient import SphinxClient
from sphinxformat.SphinxClient import rand_subset, create_forward_message
from sphinxformat.SphinxNode import SphinxNode
from sphinxformat.SphinxParams import SphinxParams


def test_send_reply():
    r = 5
    params = SphinxParams(r)

    # Create some nodes
    for i in xrange(2*r):
        SphinxNode(params)

    # Create a client
    client = SphinxClient(params)

    # Pick a list of nodes to use
    use_nodes = rand_subset(params.pki.keys(), r)

    header, delta = create_forward_message(params, use_nodes,
                                           "dest", "this is a test")

    # Send it to the first node for processing
    params.pki[use_nodes[0]].process(header, delta)

    # Create a reply block for the client
    client.create_nym("cypherpunk", r)

    # Send a message to it
    params.nymserver.send_to_nym("cypherpunk", "this is a reply")
