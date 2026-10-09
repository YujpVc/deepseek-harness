# Agent Note: Native probation decks from visual references

Status: implemented

English | [中文](2026-10-08-native-probation-reference-decks.zh.md)

## Problem

A four-page probation template can define required topics and artwork without defining the length of the finished presentation. Repeating one image-and-card layout with pre-rendered diagrams makes the body difficult to edit, duplicates photos, and obscures the source data.

## Decision

The repository-owned [generator](../../../../ppt-assistant/build_deck.py) supports `--probation` with `meta.deck_mode: native_v2`. It preserves the first template slide unchanged, retains template masters, and composes content as native text, shapes and charts. This fixed layout family accepts 13.333 × 7.5 inch templates. Content photos are deduplicated by file bytes, including copies at different paths; a paired grasp comparison can display one round's photograph in its before and after panels. The ending uses the cover layout. Strict template filling remains a separate mode.

The [evidence reader](../../../../ppt-assistant/grasp_evidence.py) reads paired depth arrays with a common crop, palette and meter range, and projects recorded grasp transforms and jaw openings with their camera calibration. Wireframes remain editable PowerPoint connectors. Display finger dimensions do not establish physical calibration or collision safety. The text checker excludes intersections between two unlabelled wireframe segments while retaining text obstruction checks.

Source photographs and their dimension-matched RGBA candidate layers can be placed as separate aligned pictures using `visual_gallery`. Each gallery has three captures with native labels; `data_table` embeds numeric comparisons in editable cells. The CLI checks alignment, transparency and rejection of mismatched layers without replacing an existing deck.

Compact depth, pose and performance cases place the prior result, solution and updated result on one page. Saved candidate scores determine which poses are shown, and candidate totals are checked against the source response. Candidate and selected-pose diagrams share native geometry and styling; unused template placeholders and empty text boxes are removed from body pages.

The delivered narrative now places WRC support before grasp engineering, and groups each optimization as prior result, solution and updated result. `pose_case` projects every candidate from the gate records with blue accepted and red rejected overlays; dense sets are rasterized in memory using the same geometry to keep the deck usable. Performance pages can state segmentation, depth completion and candidate generation timings, while `roadmap` provides near-, mid- and long-term growth columns.

## Alternatives considered

**Fill only the template's original pages.** This cannot express a complete presentation when the reference is intentionally short.

**Embed complete pre-rendered diagrams.** Their labels and data cannot be edited as PowerPoint components and impose a repeated composition.

## Verification

[CLI tests](../../../../ppt-assistant/test_build_deck.py) check unchanged cover XML, editable chart values and notes, duplicate-photo rejection, unsupported layouts, incompatible template dimensions, six paired native wireframes and rejection of mismatched opening statistics without overwriting an existing deck. [Evidence tests](../../../../ppt-assistant/test_grasp_evidence.py) check shared depth colors, invalid-depth handling, source dimensions, physical projection and preservation of real text-overlap detection. Delivered decks also require structural checks and rendered visual review.

## Consequences

The body has multiple compositions and retains editable explanations and chart data. Native layouts use explicit fields and fixed geometry; supporting another page size requires another layout family. Template decorations may repeat at the cover and ending, while body photographs may not.
