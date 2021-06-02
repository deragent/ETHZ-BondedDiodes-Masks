import gdspy

from mask.elements.test import VanDerPauwMetal, VanDerPauwContact, CTLMContact

CONTACT_WIDTH = 1000
CONTACT_SPACING = 2540
OVERHANG = 10

def Run2_TestSet(lib):

    testset = lib.new_cell('TEST_SET')

    ctlm = CTLMContact(
        lib, 'CTLM',
        [8, 16, 24, 32, 40, 48, 64, 80, 96], (3, 3),
        radius_i=100, size=400
    )

    # vdp_metal = VanDerPauwMetal(
    #     lib, 'VDPMetal',
    #     contactw=CONTACT_WIDTH, contactspacing=CONTACT_SPACING
    # )
    # vdp_contact = VanDerPauwContact(
    #     lib, 'VDPContact',
    #     contactw=CONTACT_WIDTH, contactspacing=CONTACT_SPACING, overhang=OVERHANG
    # )

    # testset.add(gdspy.CellReference(vdp_metal.cell, origin=(0, 0)))
    # testset.add(gdspy.CellReference(vdp_contact.cell, origin=(2*CONTACT_SPACING, 0)))
    testset.add(gdspy.CellReference(ctlm.cell,
        origin=(0, 0)))

    return testset
