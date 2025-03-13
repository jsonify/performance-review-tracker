# Self-Rating Implementation Todo List

## Template Updates

- [x] Update `templates/annual_review_template.md`
  - [x] Add Rating Scale definition section at the top
  - [x] Create Self Rating section template
  - [x] Add example rating justification format
  - [x] Verify Markdown formatting

## System Prompt Modifications

- [x] Update `.roo/system-prompt-annual-analyst`
  - [x] Add rating analysis requirements
  - [x] Include rating scale definitions
  - [x] Add rating justification guidelines
  - [x] Update quality checks section
  - [x] Test prompt with sample data

## Data Processing Updates

- [x] Modify core data processing
  - [x] Add rating field to data structure
  - [x] Implement rating validation (1-3)
  - [x] Update JSON output format
  - [x] Add validation for rating justification
  - [x] Update error handling for rating validation

## Report Generation Updates

- [x] Update report generation
  - [x] Modify Roo Code analysis prompt to include ratings
  - [x] Update format template with rating sections
  - [x] Add rating scale definitions to output
  - [x] Include rating validation in processing

## Documentation

- [x] Rating System Documentation
  - [x] Defined clear criteria for each rating level (1-Poor, 2-Good, 3-Excellent)
  - [x] Added examples in template
  - [x] Included rating justification requirements
  - [x] Updated system prompt with rating guidelines

## Testing and Validation

- [x] Implement core validation
  - [x] Added rating value validation (1-3)
  - [x] Added rating justification validation
  - [x] Updated data processing validation
  - [x] Added error messaging for invalid ratings

## Next Steps

1. Manual Testing
   - [x] Test with sample data
   - [x] Verify rating validation works
   - [x] Check error messages
   - [x] Test report generation

2. Documentation Updates
   - [ ] Update README with rating system info
   - [ ] Create user guide for rating system
   - [ ] Document validation requirements
   - [ ] Add examples of valid inputs

3. Final Steps
   - [ ] Test with real accomplishment data
   - [ ] Get user feedback
   - [ ] Make any necessary adjustments
   - [ ] Document any known limitations

## Notes

- Maintain consistent Markdown formatting throughout all updates
- Test after each major change
- Keep detailed notes of any issues encountered
- Document all decisions and rationales
