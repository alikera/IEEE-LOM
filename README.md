# IEEE-LOM Metadata Extractor for Learning Objects

This Python project focuses on extracting IEEE Learning Object Metadata (LOM) from educational content provided in the form of PowerPoint presentations and PDF files. The project utilizes various libraries and modules to process the content and generate metadata in JSON format. Here's a brief overview of the project:

## Project Overview
The primary objective of this project is to extract metadata from educational materials to enhance their searchability and accessibility. The extracted metadata includes information about interactivity level, semantic density, intended end-user role, context, difficulty, typical age range, typical learning time, description, language, and more. The project works with both PowerPoint presentations and PDF files, processing the content to generate meaningful metadata.

## Project Structure
- **`process_slide.py`**: Contains functions to process PowerPoint presentations and extract metadata related to interactivity, semantic density, context, difficulty, age range, learning time, description, and language.
- **`process_pdf.py`**: Handles processing of PDF files and metadata extraction.
- **`process_all.py`**: Includes functions to calculate semantic density, detect language, and estimate the age range of content.
- **`assets`**: Directory containing PowerPoint presentations and PDF files for metadata extraction.
- **`metadatas`**: Directory where extracted metadata files in JSON format are saved.

## How to Use
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/your-repository.git
   cd your-repository
   ```

2. **Install Dependencies:**
   Ensure you have Python installed. Install the required libraries using `pip`:
   ```bash
   pip install python-pptx nltk spacy textstat
   ```

3. **Run the Project:**
   - Place your PowerPoint presentations and PDF files inside the `assets` directory.
   - Execute the Python script to extract metadata:
   ```bash
   python main.py
   ```

4. **View Extracted Metadata:**
   The extracted IEEE-LOM metadata will be saved as JSON files in the `metadatas` directory.

Feel free to explore and modify the code to suit your specific requirements for extracting IEEE-LOM metadata from learning objects. For any issues or improvements, please create a GitHub issue or submit a pull request. Happy coding!
