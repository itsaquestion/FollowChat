import re
def split_and_check_with_delimiter_v3(sentence, delimiter_pattern, delimiter):
    # Split the sentence using the given delimiter pattern
    parts = re.split(delimiter_pattern, sentence)
    
    # If the split resulted in valid parts, reconstruct with the delimiter
    if all(len(part.split()) > 3 for part in parts) and len(parts) > 1:
        # Join the parts with the delimiter moved to the beginning of the next part and ensure there's space
        return [parts[0].strip()] + [delimiter.strip() + ' ' + part.strip() for part in parts[1:]]
    return [sentence]

def split_paragraph(paragraph):
    # Step 1: Split by sentences
    sentences = re.split(r'(?<=[.!?])\s+', paragraph)
    
    final_sentences = []
    
    # Common delimiters with their patterns
    delimiters = {
        r',\s*': ',',
        #r'\sand\s': 'and',
        r'\sbut\s': 'but',
        #r'\sor\s': 'or',
        #r'\snor\s': 'nor',
        r'\sfor\s': 'for',
        r'\sso\s': 'so',
        r'\syet\s': 'yet',
        r'\safter\s': 'after',
        r'\salthough\s': 'although',
        r'\sas\s': 'as',
        r'\sbecause\s': 'because',
        r'\sbefore\s': 'before',
        r'\seven if\s': 'even if',
        r'\seven though\s': 'even though',
        r'\sif\s': 'if',
        r'\sonce\s': 'once',
        r'\ssince\s': 'since',
        r'\sunless\s': 'unless',
        r'\suntil\s': 'until',
        r'\swhen\s': 'when',
        r'\swhenever\s': 'whenever',
        r'\swhereas\s': 'whereas',
        r'\swhile\s': 'while',
        r'-': '-',
        r'\sby\s': 'by'
    }
    
    for sentence in sentences:
        subs = [sentence]
        for delimiter_pattern, delimiter in delimiters.items():
            new_subs = []
            for sub in subs:
                new_subs.extend(split_and_check_with_delimiter_v3(sub, delimiter_pattern, delimiter))
            subs = new_subs
        final_sentences.extend(subs)
    
    return final_sentences

# Test the function with the new requirements

if __name__ == '__main__':
    test_paragraph_2 = "Ride sharing services like Uber and Lyft have rapidly grown in popularity over the last decade. They provide an alternative to traditional taxi services by allowing drivers to connect with riders directly through a mobile app. Economically, ride sharing brings both benefits and drawbacks. On the one hand, it increases competition in the market, which can drive down prices for consumers. The flexible work opportunities also allow more people to earn income as drivers. However, there are concerns about driver wages and benefits. Most drivers are considered independent contractors without employment protections. The long-term profitability of ride sharing companies is also uncertain. Ultimately, ride sharing is disrupting established transportation models - whether this disruption will be positive or negative remains to be seen."
    print(split_paragraph(test_paragraph_2))
