"""
This module contains tests for the fsm module.
"""
from textwrap import dedent

from auto_dev.fsm.fsm import FsmSpec

EXAMPLE = """
alphabet_in:
- DONE
- NO_MAJORITY
- RESET_TIMEOUT
- ROUND_TIMEOUT
default_start_state: RegistrationRound
final_states: []
label: HelloWorldAbciApp
start_states:
- RegistrationRound
states:
- CollectRandomnessRound
- PrintMessageRound
- RegistrationRound
- ResetAndPauseRound
- SelectKeeperRound
transition_func:
  (CollectRandomnessRound, DONE): SelectKeeperRound
  (CollectRandomnessRound, NO_MAJORITY): CollectRandomnessRound
  (CollectRandomnessRound, ROUND_TIMEOUT): CollectRandomnessRound
  (PrintMessageRound, DONE): ResetAndPauseRound
  (PrintMessageRound, ROUND_TIMEOUT): RegistrationRound
  (RegistrationRound, DONE): CollectRandomnessRound
  (ResetAndPauseRound, DONE): CollectRandomnessRound
  (ResetAndPauseRound, NO_MAJORITY): RegistrationRound
  (ResetAndPauseRound, RESET_TIMEOUT): RegistrationRound
  (SelectKeeperRound, DONE): PrintMessageRound
  (SelectKeeperRound, NO_MAJORITY): RegistrationRound
  (SelectKeeperRound, ROUND_TIMEOUT): RegistrationRound
"""


def test_from_fsm_spec():
    """Test that we can create a FsmSpec from a yaml string."""
    fsm_spec = FsmSpec.from_yaml(EXAMPLE)
    assert fsm_spec.default_start_state == "RegistrationRound"
    assert fsm_spec.states == [
        "CollectRandomnessRound",
        "PrintMessageRound",
        "RegistrationRound",
        "ResetAndPauseRound",
        "SelectKeeperRound",
    ]


def test_to_mermaid():
    """Test that we cam convert a FsmSpec to a mermaid string."""
    fsm_spec = FsmSpec.from_yaml(EXAMPLE)
    mermaid = fsm_spec.to_mermaid()
    assert mermaid == dedent(
        """
    graph TD
      RegistrationRound
      CollectRandomnessRound
      PrintMessageRound
      RegistrationRound
      ResetAndPauseRound
      SelectKeeperRound
      CollectRandomnessRound -->|DONE| SelectKeeperRound
      CollectRandomnessRound -->|NO_MAJORITY| CollectRandomnessRound
      CollectRandomnessRound -->|ROUND_TIMEOUT| CollectRandomnessRound
      PrintMessageRound -->|DONE| ResetAndPauseRound
      PrintMessageRound -->|ROUND_TIMEOUT| RegistrationRound
      RegistrationRound -->|DONE| CollectRandomnessRound
      ResetAndPauseRound -->|DONE| CollectRandomnessRound
      ResetAndPauseRound -->|NO_MAJORITY| RegistrationRound
      ResetAndPauseRound -->|RESET_TIMEOUT| RegistrationRound
      SelectKeeperRound -->|DONE| PrintMessageRound
      SelectKeeperRound -->|NO_MAJORITY| RegistrationRound
      SelectKeeperRound -->|ROUND_TIMEOUT| RegistrationRound
    """
    )


def test_from_mermaid():
    """Test that we can create a FsmSpec from a mermaid string."""
    fsm_spec = FsmSpec.from_yaml(EXAMPLE)
    mermaid = fsm_spec.to_mermaid()
    fsm_spec_from_mermaid = FsmSpec.from_mermaid(mermaid)

    # we check the atrtibutes
    assert fsm_spec_from_mermaid.default_start_state == fsm_spec.default_start_state
    assert fsm_spec_from_mermaid.states == fsm_spec.states
    assert fsm_spec_from_mermaid.alphabet_in == fsm_spec.alphabet_in
    assert fsm_spec_from_mermaid.transition_func == fsm_spec.transition_func


def test_to_string():
    """We test whether to output of to_string will match EXAMPLE"""
    fsm_spec = FsmSpec.from_yaml(EXAMPLE)
    new_fsm = fsm_spec.to_string()
    new_fsm_spec = FsmSpec.from_yaml(new_fsm)
    assert fsm_spec.default_start_state == new_fsm_spec.default_start_state
    assert fsm_spec.states == new_fsm_spec.states
    assert fsm_spec.alphabet_in == new_fsm_spec.alphabet_in
    assert fsm_spec.transition_func == new_fsm_spec.transition_func
