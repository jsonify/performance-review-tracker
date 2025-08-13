# Sample Criteria Data for Form Testing

This file contains sample data you can use to quickly test the new form-based criteria entry system.

## Annual Review Criteria Examples

### Section 1: Leadership & Influence
- **Name:** Leadership
- **Description:** Demonstrates leadership capabilities and influences team direction positively
- **Weight:** 25

### Section 2: Technical Excellence
- **Name:** Technical Excellence
- **Description:** Maintains high technical standards and drives best practices
- **Weight:** 20

### Section 3: Collaboration & Communication
- **Name:** Collaboration
- **Description:** Works effectively with team members and communicates clearly across all levels
- **Weight:** 20

### Section 4: Innovation & Problem Solving
- **Name:** Innovation
- **Description:** Introduces creative solutions and continuously improves existing processes
- **Weight:** 15

### Section 5: Business Impact
- **Name:** Business Impact
- **Description:** Contributes to measurable business outcomes and understands the bigger picture
- **Weight:** 20

## Competency Criteria Examples

### Competency 1: Programming/Software Development
- **Name:** Programming
- **Description:** Software development and coding skills across multiple technologies
- **Level 1:** Learning basic programming concepts and syntax with guidance
- **Level 2:** Developing programming skills and building simple applications
- **Level 3:** Writing production-quality code independently with consistent results
- **Level 4:** Advanced programming expertise, mentoring others and architecting solutions
- **Level 5:** Leading programming initiatives, setting standards, and driving technical innovation

### Competency 2: Problem Management
- **Name:** Problem Management
- **Description:** Issue resolution, debugging, and systematic troubleshooting capabilities
- **Level 1:** Identifying problems and escalating appropriately
- **Level 2:** Solving routine issues with some guidance
- **Level 3:** Independently resolving complex problems using systematic approaches
- **Level 4:** Expert problem solver, handling critical issues and teaching methodologies
- **Level 5:** Leading problem management processes and strategic troubleshooting initiatives

### Competency 3: Solution Architecture
- **Name:** Solution Architecture
- **Description:** System design, technical architecture, and platform decision-making
- **Level 1:** Understanding basic architecture concepts and patterns
- **Level 2:** Contributing to architecture discussions and implementing designs
- **Level 3:** Designing coherent solutions for moderate complexity systems
- **Level 4:** Advanced architecture skills, leading technical design and review processes
- **Level 5:** Setting architectural vision, driving technical strategy across multiple systems

### Competency 4: Project Management
- **Name:** Project Management
- **Description:** Planning, execution, resource management, and successful project delivery
- **Level 1:** Supporting project activities and understanding project processes
- **Level 2:** Managing small projects and contributing to larger project efforts
- **Level 3:** Successfully leading projects of moderate complexity end-to-end
- **Level 4:** Expert project manager, handling complex projects and mentoring others
- **Level 5:** Leading strategic project initiatives and establishing project management standards

## Quick Test Workflow

1. **Start the UI:** `./scripts/run_ui.sh`
2. **Go to Step 1:** Navigate to the "Review Criteria Configuration" section
3. **Test Annual Review:**
   - Select "Enter Manually" for Annual Review Criteria
   - Copy the data from the examples above
   - Add each section using the form
   - See them appear in the "Entered Criteria" display
   - Try editing and deleting entries
   - Click "Save All Criteria"
4. **Test Competency Criteria:**
   - Select "Enter Manually" for Competency Criteria  
   - Copy the data from the examples above
   - Add each competency using the form (all 5 levels required)
   - See them appear in the "Entered Competencies" display
   - Try editing and deleting entries
   - Click "Save All Competencies"
5. **Continue with normal workflow** to generate your performance review

## Features to Test

- **Form Validation:** Try submitting empty fields or duplicate names
- **Real-time Display:** Watch criteria appear as you add them
- **Edit Functionality:** Click edit buttons to modify existing criteria
- **Delete Functionality:** Remove criteria with confirmation prompts
- **Save Process:** Confirm the criteria are saved and can be used in analysis
- **Mix & Match:** Upload one criteria type, manually enter the other