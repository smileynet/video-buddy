# Narration starting points: fit, setup and cost

Checked 27 October 2026 against current first-party pages. Documentary check only: no account, checkout, SDK installation or paid request was used.

## Verified pricing and product facts

**High confidence — displayed features; checkout total unverified.** The [ElevenLabs creative pricing page](https://elevenlabs.io/pricing) lists Free at $0/month with 10k credits and three Studio projects. Starter adds Instant Voice Cloning and commercial-license features, with 30k credits and20 Studio projects. The rendered Starter card displays a $6 amount beside a first-month83%-off offer and $1 amount. Treat $6/month as the displayed pre-promotion comparison amount, not a guaranteed renewal quote; confirm actual billing, taxes and eligibility at checkout. The page also has an expired-looking September30 banner alongside an UntilNov1 offer, so avoid basing a recommendation on promotional urgency.

Supporting snippets (25words total): “$0 per month”; “3 Projects in Studio”; “10k credits per month”; “$6 First month 83% off”; “Commercial License”; “Instant Voice Cloning”.

**High confidence — public headline rate; account charge unverified.** [ElevenAPI pricing](https://elevenlabs.io/pricing/api) advertises v4 at $0.08 per1K characters and v4Turbo at $0.04. These are public pricing-card figures, not a quote for the user's selected account, plan, model, taxes or retries. Do not infer included finished-audio hours from a credit balance, or assume that using the SDK removes generation charges.

Supporting snippets: “$0.08”; “Price per 1K characters”.

**High confidence — documented browser editor.** [Studio documentation](https://elevenlabs.io/docs/eleven-creative/products/studio) documents audio/video projects, script upload, paragraph generation/regeneration, editing and export. Most new projects default to Multilingualv2; choose the desired model explicitly. Studio's quality/export entitlements must be checked in its own documentation rather than copied from API output-format rules.

Supporting snippet: “Create video and audio projects with Studio.”

Version: live pricing and Studio4.0 documentation checked on the date above; no pinned product release or account capability validated.

## Fit recommendation — reasoned assessment, not benchmark

| Choice | Fit | Setup complexity | Cost framing |
|---|---|---|---|
| **Recommend first: ElevenLabs Studio audio project** | First short prerecorded narration and a single revision; hosted audio acceptable | Low relative setup: browser account/editor, no custom client | Free can introduce the editor with available voices/credits. For this guide's own-voice clone, Instant Voice Cloning is listed under paid Starter. Check actual plan features and cost before generating. |
| **Choose for repeatable automation: official SDK plus joining tools** | Batches, file manifests, integration and controlled revision workflows | Higher: code, SDK version, credentials, saved takes, retry/acceptance logic, join/timing checks | Provider usage remains billable according to account/model; add engineering and maintenance time. A free library is not free voice generation. |

This weighting prioritizes the user's stated job, then minimizes initial setup, then checks total trial/operating cost. It does not establish a universal cheapest or best-quality product. If audio must remain local, both hosted choices fail that constraint; define a separate local trial rather than silently recommending either. SDK stitching and FFmpeg are components of the automation route, not competing complete products.

## Suggested guide wording

“Recommended starting point: ElevenLabs Studio, a browser-based audio editor. Use it to make and revise one short passage before writing automation. You can explore with its Free tier; cloning your own voice is a paid feature listed under Starter. Confirm the current plan and generation cost in your account.”

For an exact displayed-price note, distinguish the $6 pre-promotion amount from introductory offers and link the live pricing page. Avoid promising that the free tier completes the own-voice or commercial-use task.
