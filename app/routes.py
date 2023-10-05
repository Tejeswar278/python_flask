from flask import request, jsonify, render_template
from app import app, db
from app.scraper import scrape_wikipedia
from app.models import Response as ResponseModel

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form.get('url')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        # scraped_data = scrape_wikipedia(url)
        # return jsonify(scraped_data)
        # This generator function yields content snippets as they become available
        # def generate_content():
        #     for content_snippet in scrape_wikipedia(url):
        #         yield jsonify(content_snippet) + "\n"
        
        # # Use the Response object to create a streaming response
        # return Response(generate_content(), content_type='application/json')

        # Scrape the Wikipedia page
        result = scrape_wikipedia(url)

        # Save responses to the database
        for internal_url in result:
            response = ResponseModel(url=internal_url, content="")  # Initialize with empty content
            db.session.add(response)
            db.session.commit()

        # Render the index.html template with the scraped results
        return render_template('index.html', result=result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500