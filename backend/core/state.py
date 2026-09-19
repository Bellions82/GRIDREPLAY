from enum import StrEnum
class RenderState(StrEnum):
    CREATED='CREATED'; QUEUED='QUEUED'; CLAIMED='CLAIMED'; PROCESSING='PROCESSING'; QA_PENDING='QA_PENDING'; APPROVED='APPROVED'; ASSEMBLY_PENDING='ASSEMBLY_PENDING'; COMPLETED='COMPLETED'; REGENERATE='REGENERATE'; FAILED='FAILED'
TRANSITIONS={RenderState.CREATED:{RenderState.QUEUED},RenderState.QUEUED:{RenderState.CLAIMED,RenderState.FAILED},RenderState.CLAIMED:{RenderState.PROCESSING,RenderState.QUEUED},RenderState.PROCESSING:{RenderState.QA_PENDING,RenderState.REGENERATE,RenderState.FAILED},RenderState.QA_PENDING:{RenderState.APPROVED,RenderState.REGENERATE,RenderState.FAILED},RenderState.APPROVED:{RenderState.ASSEMBLY_PENDING},RenderState.ASSEMBLY_PENDING:{RenderState.COMPLETED,RenderState.FAILED},RenderState.REGENERATE:{RenderState.QUEUED}}
def can_transition(a:RenderState,b:RenderState)->bool:return b in TRANSITIONS.get(a,set())
