import gdspy

from mask.elements.test import VanDerPauwMetal, VanDerPauwContact, TLMContact

CONTACT_WIDTH = 1000
CONTACT_SPACING = 2540
OVERHANG = 10

def Run1_TestSet(lib):

    testset = lib.new_cell('TEST_SET')

    tlm = TLMContact(
        lib, 'TLM',
        [1000, 2000, 3000, 5000, 8000, 10000, 12000, 15000],
        contactw=CONTACT_WIDTH, contactspacing=CONTACT_SPACING, overhang=OVERHANG
    )

    vdp_metal = VanDerPauwMetal(
        lib, 'VDPMetal',
        contactw=CONTACT_WIDTH, contactspacing=CONTACT_SPACING
    )
    vdp_contact = VanDerPauwContact(
        lib, 'VDPContact',
        contactw=CONTACT_WIDTH, contactspacing=CONTACT_SPACING, overhang=OVERHANG
    )

    testset.add(gdspy.CellReference(vdp_metal.cell, origin=(0, 0)))
    testset.add(gdspy.CellReference(vdp_contact.cell, origin=(2*CONTACT_SPACING, 0)))
    testset.add(gdspy.CellReference(tlm.cell,
        origin=(3.5*CONTACT_SPACING - 0.5*CONTACT_WIDTH - OVERHANG, 0)))

    return testset
