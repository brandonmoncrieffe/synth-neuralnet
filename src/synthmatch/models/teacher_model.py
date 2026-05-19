"""Future teacher model skeleton."""

from __future__ import annotations


class TeacherModel:
    """Placeholder for a larger inverse-synthesis model.

    Future work may include pretrained audio encoders, candidate parameter
    prediction, render-aware ranking, and distillation into a smaller student.
    """

    def predict_candidates(self, waveform: object) -> None:
        """Predict candidate parameter sets for a target waveform."""

        _ = waveform
        raise NotImplementedError("TODO: design teacher model after clean dataset baseline")

