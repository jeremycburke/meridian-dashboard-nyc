# Writing and Communication Rules

<!-- markdownlint-disable MD029 -- the rules keep their numbers 1 to 46 across sections -->

All text in this repository follows these rules. This includes:

- the files in `docs/` and `specs/`, the README, `AGENTS.md` and `CLAUDE.md`
- docstrings and code comments
- interface text in `web/`
- the digests and reviews that the site-review agent writes
- pull requests and commit messages

People and AI agents must read this file before they write or edit content.

The rules have two parts:

1. **Simplified Technical English (STE).** We write in ASD-STE100 Simplified Technical English. Part 1 summarizes the STE writing rules as we apply them.
2. **Writing and communication rules.** Part 2 gives the general rules for clear, natural, professional English.

If two rules conflict, the STE rule applies. No test checks these rules yet. See Part 3.

## Part 1: ASD-STE100 Simplified Technical English

ASD-STE100 is a controlled language for technical documents. It has writing rules and a dictionary of approved words. The full specification is available from the [ASD-STE100 website](https://www.asd-ste100.org). This part is a summary for this project. It does not replace the specification.

### Words

- Use simple, common words. Use "use", not "utilize". Use "start", not "commence". Use "help", not "facilitate".
- Use one word for one meaning. Do not use different words for the same thing. For example, if a page says "model", do not change to "LLM" or "engine" for the same thing.
- Use a word only with its usual meaning and as the usual part of speech.
- You can use technical names and technical verbs from our field, for example "token", "agent", "deploy" and "fine-tune". Define each new technical name in plain words the first time a document uses it.
- Do not use slang or idioms. Do not use contractions such as "don't" or "it's". Write "do not" and "it is".
- Do not use Latin abbreviations. Write "for example", not "e.g.". Write "that is", not "i.e.". Write "versus", not "vs.". Do not use "etc.".

### Noun clusters

- Do not put more than three nouns together. Break long noun clusters with a preposition or a verb. For example, write "the threshold for credit approval", not "the credit approval threshold value".

### Verbs

- Use the active voice. Use the passive voice only in descriptions when the actor is unknown or not important.
- Use simple tenses: present, simple past and simple future.
- Use a verb to show an action. Write "evaluate the model", not "perform an evaluation of the model".
- Do not use the "-ing" form as a noun or as part of a verb phrase, unless it is part of a technical name such as "prompt caching" or "tool calling".
- Use "must" for a requirement. Use "can" for a possibility or an ability. Use "do not" for a prohibition. Do not use "should", "may", "might", "could" or "would" when the meaning is not clear.

### Sentences

- Write one topic in each sentence.
- Keep instructions to 20 words or fewer.
- Keep descriptive sentences to 25 words or fewer.
- Do not remove words such as "the", "a" or "is" to make a sentence shorter.
- Use a vertical list when a sentence has a series of items or steps.
- Use words such as "if", "when", "then" and "because" to show how sentences connect.

### Procedures

- Write each instruction as a command: "Run the tests."
- Write one instruction in each sentence, unless the actions happen at the same time.
- Put a condition before the instruction: "If the build fails, read the log."
- Number the steps in the order the reader does them.
- Put a warning or a caution before the step that it applies to.

### Descriptive text

- Give the most important information first.
- Write one topic in each paragraph. Use no more than six sentences in each paragraph.
- Use headings, lists and tables to help the reader find information.
- Use an imperative heading for a task ("Choose the model"). Use a noun heading for a topic ("Success criteria"). Do not start a heading with an "-ing" word.

### Warnings and cautions

- Start a warning or a caution with a clear command. Then give the reason or the risk.
- Use a WARNING alert for a risk to people, customer data or security.
- Use a CAUTION alert for a risk to systems, money or work.

### Punctuation and word count

- Count each word, number, hyphenated word and code term as one word.
- Do not use semicolons. Write two sentences.
- Use a colon only before a list or an example.
- Use American English spelling.

## Part 2: Writing and communication rules

### Core principles

1. **Prioritize clarity over sophistication.** Use simple, precise, natural English. Avoid complicated wording when a simpler alternative communicates the same meaning.

2. **Be concise without losing meaning.** Remove unnecessary words, repetition, filler, and redundant explanations. Preserve all important details.

3. **Write like a thoughtful professional.** Use a natural, confident, direct tone. Avoid robotic, overly formal, promotional, or artificially enthusiastic language.

4. **Lead with the main point.** State the conclusion, request, decision, or important information first. Provide supporting context afterward.

5. **Use active voice by default.** Prefer "We updated the configuration" over "The configuration was updated," unless the actor is unknown or unimportant.

6. **Make every sentence useful.** Each sentence should communicate information, explain a decision, provide context, or request an action.

### Sentence construction

7. **Favor short, well-structured sentences.** Break up long sentences when doing so improves readability. Vary sentence length naturally.

8. **Use straightforward vocabulary.** Prefer common words over business jargon, academic language, and unnecessarily technical expressions.

9. **Eliminate filler phrases.** Avoid expressions such as "It is important to note that," "In order to," "I would like to mention," and "It should be noted that."

10. **Avoid unnecessary qualifiers.** Remove words such as "basically," "actually," "really," "very," and "quite" when they add no meaning.

11. **Avoid excessive hedging.** Be direct when facts are established. Express uncertainty when it is genuine and relevant.

12. **Avoid awkward or unnatural constructions.** Rewrite sentences that sound translated, overly formal, or unlike ordinary professional English.

13. **Use consistent terminology.** Refer to the same concept, component, process, or person using the same term throughout the text.

### Structure and flow

14. **Organize information logically.** Present ideas in an order that makes them easy to understand without requiring the reader to reconstruct the reasoning.

15. **Keep paragraphs focused.** Each paragraph should develop one main idea. Separate unrelated topics.

16. **Use transitions only when helpful.** Avoid unnecessary "Furthermore," "Moreover," "Additionally," and "In conclusion."

17. **Use bullets selectively.** Use lists when they improve scanning or comparison. Prefer connected prose for simple explanations.

18. **Avoid repeating information.** Do not restate the same point in the introduction, body, and conclusion unless repetition serves a clear purpose.

### Tone and style

19. **Be professional but conversational.** Aim for the tone of a capable colleague explaining something clearly.

20. **Avoid corporate buzzwords.** Replace terms such as "leverage," "synergy," "robust," "seamless," and "best-in-class" when simpler, more specific wording works.

21. **Avoid exaggerated claims.** Do not describe solutions as "revolutionary," "perfect," or "game-changing" without compelling justification.

22. **Be respectful and direct.** Avoid patronizing language, excessive politeness, unnecessary apologies, and exaggerated reassurance.

23. **Use positive, constructive language.** When describing problems, explain what is wrong, why it matters, and what should happen next.

24. **Match the audience.** Use technical language for technical readers, but explain unfamiliar concepts when writing for a broader audience.

### Technical communication

25. **Explain the outcome before the implementation.** Describe what changed or what needs to happen before explaining technical details.

26. **Be specific.** Prefer concrete descriptions over vague statements such as "There is an issue" or "Some improvements were made."

27. **Keep technical accuracy intact.** Simplify explanations without changing the intended meaning, technical terminology, constraints, or factual details.

28. **Make requests actionable.** Clearly communicate what needs to be done, who is responsible when known, and any relevant constraints or deadlines.

29. **Write useful error messages and documentation.** Explain the problem, its likely impact, and the next step when that information is available.

30. **Avoid unnecessary background information.** Include context only when it helps readers understand the problem, decision, or action.

### Editing and rewriting rules

31. **Preserve the original intent.** Improve grammar, clarity, structure, and flow without changing the underlying meaning.

32. **Do not invent information.** Never introduce unsupported facts, assumptions, commitments, dates, or conclusions while rewriting.

33. **Preserve important nuances.** Maintain distinctions between facts, assumptions, possibilities, recommendations, and decisions.

34. **Fix grammar and punctuation naturally.** Follow standard English conventions without enforcing rigid rules that make sentences awkward.

35. **Maintain the author's intended tone.** Improve the writing without making a casual message unnecessarily formal or a serious message overly casual.

36. **Prefer meaningful edits over cosmetic changes.** Do not rewrite sentences that are already clear simply to make them different.

37. **Remove ambiguity.** Make pronoun references, responsibilities, conditions, and relationships explicit when necessary.

38. **Maintain consistent spelling and formatting.** Use American English by default unless the existing content or project specifies another convention.

39. **Avoid overediting.** Make the smallest changes necessary to achieve a meaningful improvement in readability, correctness, or tone.

40. **Perform a final readability check.** Confirm that the text is accurate, natural, logically structured, concise, and easy to understand on the first reading.

### Output behavior

41. When asked to rewrite, polish, or correct text, return the improved version directly unless explanations are explicitly requested.

42. Do not add greetings, introductions, summaries, or commentary that were not part of the requested output.

43. Preserve Markdown formatting, code blocks, identifiers, URLs, file paths, and technical literals unless changes are explicitly requested.

44. For emails, messages, documentation, PR descriptions, commit messages, and technical explanations, adapt the structure and level of detail to the medium.

45. When several valid phrasings are possible, choose the most natural and straightforward one rather than the most elaborate.

46. Do not sacrifice accuracy, important context, or necessary detail merely to make the text shorter.

### Final quality standard

Before producing any written content, silently check:

- Is the main point immediately clear?
- Can any words or sentences be removed without losing meaning?
- Does the wording sound natural to a fluent English speaker?
- Is the tone appropriate for the intended audience?
- Are the statements precise, accurate, and unambiguous?
- Is the structure easy to follow?
- Have the original intent and important details been preserved?

**Default writing goal:** Produce clear, concise, precise, natural English that sounds like it was written by a competent professional, not generated from a template.

## Part 3: Checks

No automated test checks these rules yet. A person or an agent checks them in each review.

These are the limits that a machine can check:

| Check | Limit |
| --- | --- |
| Sentence length in descriptive text | 25 words or fewer |
| Sentence length in numbered steps | 20 words or fewer |
| Sentences in a paragraph | 6 or fewer |
| Banned words and filler phrases | None. Use a simpler alternative. |
| Contractions | None |
| Latin abbreviations (e.g., i.e., etc., vs.) | None |
| British spellings | None. Use American English. |

The limits do not apply to tables, code blocks, headings or link URLs. A person must also check the rules that a machine cannot check, for example active voice and one meaning for each word.
