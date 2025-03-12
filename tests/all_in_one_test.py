# import json
# import os
# import pytest
# from datetime import datetime
# import re
# from typing import List, Dict, Any, Set, Tuple

# class TestAnalystPrompt:
#     def verify_data_structure(self, sample_data):
#         """Verify sample data structure matches expected format"""
#         required_fields = ['Date', 'Title', 'Description', 'Acceptance Criteria', 
#                          'Success Notes', 'Impact']
        
#         for entry in sample_data:
#             for field in required_fields:
#                 assert field in entry, f"Missing required field: {field}"
            
#             # Verify date format
#             try:
#                 datetime.strptime(entry['Date'], '%Y-%m-%d')
#             except ValueError:
#                 raise ValueError(f"Invalid date format in entry: {entry['Title']}")
            
#             # Verify Impact values
#             assert entry['Impact'] in ['High', 'Medium', 'Low'], \
#                 f"Invalid Impact value in entry: {entry['Title']}"
        
#         return True

#     def test_data_structure(self, sample_data):
#         """Pytest function for data structure verification"""
#         assert self.verify_data_structure(sample_data)

#     def test_criteria_coverage(self, sample_data, system_prompt):
#         """Test if sample data can be mapped to defined criteria"""
#         annual_criteria = self._extract_detailed_criteria(system_prompt, 'ANNUAL REVIEWS')
#         competency_criteria = self._extract_detailed_criteria(system_prompt, 'COMPETENCY ASSESSMENTS')
        
#         # Analyze each accomplishment for criteria coverage
#         for entry in sample_data:
#             matches = self._find_criteria_matches(entry, annual_criteria, competency_criteria)
#             assert len(matches) > 0, \
#                 f"No criteria matches found for: {entry['Title']}"

#     def _extract_detailed_criteria(self, prompt: str, section: str) -> List[Dict[str, Any]]:
#         """Extract criteria with their detailed descriptions from system prompt"""
#         criteria = []
#         current_criterion = None
#         description_lines = []
#         weight = "Medium"  # Default weight
        
#         # Find section boundaries
#         lines = prompt.split('\n')
#         section_start = -1
#         next_section_start = -1
        
#         for i, line in enumerate(lines):
#             if f"For {section}" in line:
#                 section_start = i
#             elif section_start >= 0 and (line.startswith('For ') or line.startswith('====')):
#                 next_section_start = i
#             break
        
#         if section_start == -1:
#             return []
            
#         if next_section_start == -1:
#             next_section_start = len(lines)
        
#         # Process only lines within this section
#         for i in range(section_start, next_section_start):
#             line = lines[i].strip()
            
#             # Skip empty lines and section headers
#             if not line or f"For {section}" in line or line.endswith(':'):
#                 continue
                
#             # Check for weight indicators
#             if "(High Priority)" in line or "(Core)" in line:
#                 weight = "High"
#             elif "(Medium Priority)" in line:
#                 weight = "Medium"
            
#             # Look for numbered criteria entries
#             numbered_match = re.match(r'^\d+\.\s+([^(]+).*$', line)
#             if numbered_match:
#                 # Save previous criterion if exists
#                 if current_criterion:
#                     criteria.append(self._create_criterion_entry(current_criterion, description_lines, weight))
                
#                 # Start new criterion
#                 current_criterion = numbered_match.group(1).strip()
#                 description_lines = []
#                 continue
            
#             # Collect bullet points and descriptions
#             if line.startswith('-'):
#                 description_lines.append(line[1:].strip())
#             else:
#                 description_lines.append(line)
        
#         # Add the last criterion if exists
#         if current_criterion:
#             criteria.append(self._create_criterion_entry(current_criterion, description_lines, weight))
        
#         return criteria

#     def _create_criterion_entry(self, name: str, description_lines: List[str], weight: str) -> Dict[str, Any]:
#         """Create a criterion entry with extracted terms and keywords"""
#         return {
#             'name': name,
#             'description': ' '.join(description_lines),
#             'keywords': self._extract_keywords(' '.join([name] + description_lines)),
#             'primary_terms': self._extract_primary_terms(name, description_lines),
#             'weight': weight
#         }

#     def _extract_primary_terms(self, criterion_name: str, description_lines: List[str]) -> Dict[str, float]:
#         """Extract primary terms that must be present for a strong match, with importance weights"""
#         terms = {}
        
#         # Add main criterion name components with high weights
#         name_parts = criterion_name.lower().split()
#         full_name = ' '.join(name_parts)
#         terms[full_name] = 1.0  # Full name gets highest weight
        
#         # Add consecutive word combinations with descending weights
#         for i in range(len(name_parts)):
#             for j in range(i + 1, min(i + 4, len(name_parts) + 1)):
#                 term = ' '.join(name_parts[i:j])
#                 if len(term) > 3 and term != full_name:
#                     terms[term] = 0.8 if j - i > 1 else 0.6
        
#         # Define specialized pattern sets for different types of criteria
#         quality_patterns = {
#             r'\b(?:comprehensive|detailed|thorough)\b': 0.7,
#             r'\b(?:high[- ]quality|excellent|exceptional)\b': 0.8,
#             r'\b(?:consistent|reliable|accurate)\b': 0.7,
#             r'\b(?:approved|validated|complete)\b': 0.6,
#             r'\b(?:quality|performance|efficiency)\b': 0.8
#         }
        
#         technical_patterns = {
#             r'\b(?:design\s+document|technical\s+spec(?:ification)?|architecture\s+design)\b': 1.0,
#             r'\b(?:system\s+design|solution\s+architecture|implementation\s+plan)\b': 1.0,
#             r'\b(?:designs?|architect(?:ure)?|develop(?:ment)?|implement(?:ation)?)\b': 0.8,
#             r'\b(?:technical|system|solution|performance)\b': 0.7
#         }
        
#         documentation_patterns = {
#             r'\b(?:document(?:ation)?|specification|blueprint)\b': 0.8,
#             r'\b(?:requirements?|plans?|models?)\b': 0.7,
#             r'\b(?:review(?:ed)?|feedback|approval)\b': 0.6
#         }
        
#         project_patterns = {
#             r'\b(?:manage[ds]?|coordinate[ds]?|lead[s]?)\b': 0.8,
#             r'\b(?:plan(?:ning)?|organize[ds]?|deliver(?:y|ed)?)\b': 0.7,
#             r'\b(?:stakeholder|timeline|milestone)\b': 0.6
#         }
        
#         # Select pattern set based on criterion type
#         criterion_lower = criterion_name.lower()
#         patterns = {}
        
#         if 'quality' in criterion_lower:
#             patterns.update(quality_patterns)
#         elif any(term in criterion_lower for term in ['design', 'technical', 'architecture']):
#             patterns.update(technical_patterns)
#         elif any(term in criterion_lower for term in ['document', 'specification']):
#             patterns.update(documentation_patterns)
#         elif any(term in criterion_lower for term in ['manage', 'project', 'lead']):
#             patterns.update(project_patterns)
#         else:
#             patterns = {**quality_patterns, **technical_patterns}
        
#         # Process description text
#         desc_text = ' '.join(description_lines).lower()
#         for pattern, weight in patterns.items():
#             matches = re.findall(pattern, desc_text)
#             for match in matches:
#                 if match not in terms or terms[match] < weight:
#                     terms[match] = weight
        
#         return terms

#     def _normalize_term(self, term: str) -> str:
#         """Normalize a term by removing common suffixes and converting to singular form"""
#         term = term.lower().strip()
        
#         # Dictionary of known term variations
#         known_variations = {
#             'quality': ['qualities', 'qualitative'],
#             'quantity': ['quantities', 'quantitative'],
#             'technical': ['technically', 'technique'],
#             'document': ['documentation', 'documenting', 'documented'],
#             'implement': ['implementation', 'implementing', 'implemented'],
#             'design': ['designing', 'designed', 'designs'],
#             'review': ['reviewing', 'reviewed', 'reviews'],
#             'system': ['systematic', 'systems'],
#             'architecture': ['architectural', 'architectures'],
#             'perform': ['performance', 'performing', 'performed']
#         }
        
#         # Check for known variations first
#         for base, variations in known_variations.items():
#             if term in variations or term == base:
#                 return base
        
#         # Keep common quality-related terms intact
#         quality_terms = {'comprehensive', 'detailed', 'thorough', 'effective', 'efficient'}
#         if term in quality_terms:
#             return term
        
#         # Handle common suffixes carefully
#         if term.endswith('ing') and len(term) > 5:
#             return term[:-3]
#         if term.endswith('tion') and len(term) > 6:
#             return term[:-4] + 'e'
#         if term.endswith('ment') and len(term) > 6:
#             return term[:-4]
#         if term.endswith('ed') and len(term) > 4:
#             return term[:-2]
#         if term.endswith('ly') and len(term) > 4:
#             return term[:-2]
#         if term.endswith('s') and not term.endswith('ss'):
#             return term[:-1]
        
#         return term

#     def _calculate_match_confidence(self, text: str, entry_keywords: Set[str],
#                                  criterion: Dict[str, Any], impact: str) -> float:
#         """Calculate confidence score for a criterion match using weighted primary terms"""
#         text = text.lower()
        
#         # Quality indicators boost
#         quality_boost = 0.0
#         indicator_boosts = {
#             # Documentation quality (0.25)
#             'comprehensive document': 0.25,
#             'detailed document': 0.25,
#             'technical specification': 0.25,
#             'design document': 0.25,
#             
#             # Strong quality indicators (0.2)
#             'comprehensive': 0.2,
#             'excellent': 0.2,
#             'exceptional': 0.2,
#             'high-quality': 0.2,
#             'high quality': 0.2,
            
#             # Technical quality (0.2)
#             'technical excellence': 0.2,
#             'architectural design': 0.2,
#             'system design': 0.2,
            
#             # Medium quality indicators (0.15)
#             'detailed': 0.15,
#             'thorough': 0.15,
#             'effective': 0.15,
#             'efficient': 0.15,
#             'reliable': 0.15,
#             'consistent': 0.15,
#             'complete': 0.15,
#             'approved': 0.15
#         }
        
#         # Calculate base boost
#         base_boost = 0.0
#         found_indicators = []
        
#         for indicator, weight in indicator_boosts.items():
#             if indicator in text:
#                 base_boost = max(base_boost, weight)
#                 found_indicators.append(indicator)
        
#         # Additional boost for multiple indicators
#         if len(found_indicators) > 1:
#             base_boost *= (1 + 0.1 * min(len(found_indicators) - 1, 3))
        
#         # Context-specific boosts
#         criterion_name = criterion['name'].lower()
        
#         # Quality criterion gets extra boost from documentation terms
#         if 'quality' in criterion_name:
#             doc_terms = ['document', 'specification', 'design']
#             if any(term in text for term in doc_terms):
#                 base_boost *= 1.2
        
#         # Technical criteria get boost from technical quality terms
#         if any(term in criterion_name for term in ['technical', 'system', 'architecture']):
#             tech_terms = ['technical', 'architecture', 'system', 'design']
#             if any(term in text for term in tech_terms):
#                 base_boost *= 1.15
        
#         # Calculate primary terms score
#         primary_score = 0.0
#         max_score = 0.0
#         for term, weight in criterion['primary_terms'].items():
#             max_score += weight
#             if term in text:
#                 primary_score += weight
        
#         # Calculate primary terms ratio
#         primary_ratio = primary_score / max_score if max_score > 0 else 0
        
#         # Calculate keyword match ratio
#         normalized_text = set(self._normalize_term(word) for word in text.split())
#         normalized_keywords = set(self._normalize_term(k) for k in criterion['keywords'])
#         keyword_matches = normalized_text & normalized_keywords
#         keyword_score = len(keyword_matches) / len(normalized_keywords) if normalized_keywords else 0
        
#         # Calculate base confidence
#         base_confidence = (0.6 * primary_ratio + 0.4 * keyword_score)
        
#         # Add quality boost
#         confidence = base_confidence + quality_boost
        
#         # Weight and impact boosts
#         weight_factors = {'High': 1.2, 'Medium': 1.0, 'Low': 0.8}
#         confidence *= weight_factors.get(criterion['weight'], 1.0)
        
#         if impact == 'High' and criterion['weight'] == 'High':
#             confidence *= 1.2
        
#         # Technical design boost
#         if any(term in text for term in ['technical', 'design', 'architecture', 'system']):
#             if any(term in criterion_name for term in ['technical', 'system', 'architecture']):
#                 confidence *= 1.25
        
#         # Documentation quality boost
#         if 'document' in text and any(term in criterion_name for term in ['quality', 'technical']):
#             confidence *= 1.15
        
#         return min(confidence, 1.0)

#     def verify_data_structure(self, sample_data):
#         """Verify sample data structure matches expected format"""
#         required_fields = ['Date', 'Title', 'Description', 'Acceptance Criteria', 
#                          'Success Notes', 'Impact']
        
#         for entry in sample_data:
#             for field in required_fields:
#                 assert field in entry, f"Missing required field: {field}"
            
#             # Verify date format
#             try:
#                 datetime.strptime(entry['Date'], '%Y-%m-%d')
#             except ValueError:
#                 raise ValueError(f"Invalid date format in entry: {entry['Title']}")
            
#             # Verify Impact values
#             assert entry['Impact'] in ['High', 'Medium', 'Low'], \
#                 f"Invalid Impact value in entry: {entry['Title']}"
        
#         return True

#     def test_data_structure(self, sample_data):
#         """Pytest function for data structure verification"""
#         assert self.verify_data_structure(sample_data)

#     def test_criteria_coverage(self, sample_data, system_prompt):
#         """Test if sample data can be mapped to defined criteria"""
#         annual_criteria = self._extract_detailed_criteria(system_prompt, 'ANNUAL REVIEWS')
#         competency_criteria = self._extract_detailed_criteria(system_prompt, 'COMPETENCY ASSESSMENTS')
        
#         for entry in sample_data:
#             matches = self._find_criteria_matches(entry, annual_criteria, competency_criteria)
#             assert len(matches) > 0, f"No criteria matches found for: {entry['Title']}"