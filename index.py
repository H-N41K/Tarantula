from flask import Flask, render_template, request, redirect, session, flash
import Searcher, AjaxUpdater 
import math
app = Flask('Tarantula Server')
app.secret_key = "INSY_WINSY"
@app.route("/")
def main():
	
	return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
	searcher = Searcher.Searcher('google.db')
	if request.method == 'GET':
		term = request.args.get('term')
		if term == '':
			return('Please enter a search query')
		type1 = request.args.get('type')
		if request.args.get('page') != None: page = request.args.get('page')
		else: page = 1 
		if type1 == 'web':
			searchType = request.args.get('searchType')
			if searchType ==  'lucky':
				luckyUrl = searcher.getLuckySiteResult(term.lower())
				return redirect(str(luckyUrl))
			else:
				numResults, searchTime, resultsHtml, pageSize = searcher.getSiteResultsHtml(page, term.lower())
				pagesToShow = 10
				paginationContainer =''
				page = int(page)	
				numPages = math.ceil(int(numResults)/int(pageSize))
				pagesLeft = min(int(pagesToShow), int(numPages))
				currentPage = page - math.floor(int(pagesToShow)/2)

				if currentPage < 1 : currentPage = 1
				if (currentPage + pagesLeft > numPages + 1): currentPage = numPages -pagesLeft +1
				while pagesLeft != 0 and currentPage <= numPages:
					if currentPage == page:
						paginationContainer += f'''<div class='pageNumberContainer'>
							<img src='static/images/logoPageNumber.png' width='16px' height='16px' style='filter:saturate(8);'>
							<span class='pageNumber' style='color:#c00909;font-weight:bold;'>{currentPage}</span>
						</div>'''
					else:
						paginationContainer += f'''<div class='pageNumberContainer'>
							<a href='/search?term={term}&type={type1}&page={currentPage}'>
							<img src='static/images/logoPageNumber.gif' width='16px' height='16px'>
							<span class='pageNumber'>{currentPage}</span>
							</a>
						</div>'''
					currentPage += 1
					pagesLeft -= 1
				return render_template('search.html', term=term,type1=type1,searchTime=searchTime,numResults=numResults,resultsHtml=resultsHtml,numPages=numPages,pagesLeft=pagesLeft,currentPage=currentPage,paginationContainer=paginationContainer)
		elif type1 == 'images':
			numResults = searcher.getImageNumResults(term.lower())
			searchTime, resultsHtml, pageSize= searcher.getImageResultsHtml(page, term.lower())
			pagesToShow = 10
			paginationContainer =''
			page = int(page)	
			numPages = math.ceil(int(numResults)/int(pageSize))
			pagesLeft = min(int(pagesToShow), int(numPages))
			currentPage = page - math.floor(int(pagesToShow)/2)

			if currentPage < 1 : currentPage = 1
			if (currentPage + pagesLeft > numPages + 1): currentPage = numPages -pagesLeft +1
			while pagesLeft != 0 and currentPage <= numPages:
				if currentPage == page:
					paginationContainer += f'''<div class='pageNumberContainer'>
						<img src='static/images/logoPageNumber.png' width='16px' height='16px' style='filter:saturate(8);'>
						<span class='pageNumber' style='color:#c00909;font-weight:bold;'>{currentPage}</span>
					</div>'''
				else:
					paginationContainer += f'''<div class='pageNumberContainer'>
						<a href='/search?term={term}&type={type1}&page={currentPage}'>
						<img src='static/images/logoPageNumber.gif' width='16px' height='16px'>
						<span class='pageNumber'>{currentPage}</span>
						</a>
					</div>'''
				currentPage += 1
				pagesLeft -= 1
			return render_template('search.html', term=term,type1=type1,searchTime=searchTime,numResults=numResults,resultsHtml=resultsHtml,numPages=numPages,pagesLeft=pagesLeft,currentPage=currentPage,paginationContainer=paginationContainer)
			# return 'COMING SOON!!'
		elif type1 == 'torrents':
			numResults = searcher.getTorrentNumResults(term.lower())
			searchTime, resultsHtml, pageSize= searcher.getTorrentResultsHtml(page, term.lower())
			pagesToShow = 10
			paginationContainer =''
			page = int(page)	
			numPages = math.ceil(int(numResults)/int(pageSize))
			pagesLeft = min(int(pagesToShow), int(numPages))
			currentPage = page - math.floor(int(pagesToShow)/2)

			if currentPage < 1 : currentPage = 1
			if (currentPage + pagesLeft > numPages + 1): currentPage = numPages -pagesLeft +1
			while pagesLeft != 0 and currentPage <= numPages:
				if currentPage == page:
					paginationContainer += f'''<div class='pageNumberContainer'>
						<img src='static/images/logoPageNumber.png' width='16px' height='16px' style='filter:saturate(8);'>
						<span class='pageNumber' style='color:#c00909;font-weight:bold;'>{currentPage}</span>
					</div>'''
				else:
					paginationContainer += f'''<div class='pageNumberContainer'>
						<a href='/search?term={term}&type={type1}&page={currentPage}'>
						<img src='static/images/logoPageNumber.gif' width='16px' height='16px'>
						<span class='pageNumber'>{currentPage}</span>
						</a>
					</div>'''
				currentPage += 1
				pagesLeft -= 1
			return render_template('search.html', term=term,type1=type1,searchTime=searchTime,numResults=numResults,resultsHtml=resultsHtml,numPages=numPages,pagesLeft=pagesLeft,currentPage=currentPage,paginationContainer=paginationContainer)
		else:
			return '404'	

@app.route('/ajax/updateImageCount', methods=['POST'])
def updateImageCount():
	if request.method == 'POST':
		if request.form['imageUrl'] == '':
			print('BLANK URL')
			return ''
		print(f'URL of Image Clicked :: {request.form["imageUrl"]}')
		ajaxUpdater = AjaxUpdater.AjaxUpdater('google.db')
		updateImageStatus = ajaxUpdater.updateImageCount(request.form['imageUrl'])
	return ''

@app.route('/ajax/setBroken', methods=['POST'])
def setBroken():
	if request.method == 'POST':
		if request.form['src'] == '':
			print('BLANK URL')
			return '' #Error
		print(f'Broken URL :: {request.form["src"]}')
		ajaxUpdater = AjaxUpdater.AjaxUpdater('google.db')
		setBrokenStatus = ajaxUpdater.setBroken(request.form['src'])
		return request.form['src']	
	return ''
if __name__ == "__main__":
    app.run(debug=True)