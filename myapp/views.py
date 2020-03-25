from django.shortcuts import render_to_response
from django.template import RequestContext
from myapp.forms import UploadFileForm
from PIL import Image, ImageOps,ImageFilter
from s3_client import s3_client

def applyfilter(filename, preset):
	inputfile = '/home/ec2-user/AWSImagePro/media/' + filename

	f=filename.split('.')
	outputfilename = f[0] + '_' + preset + '_out.jpg'

	outputfile = '/home/ec2-user/AWSImagePro/myapp/templates/static/output/' + outputfilename

	im = Image.open(inputfile)
	if preset=='gray':
		im = ImageOps.grayscale(im)
	if preset=='edge':
		im = ImageOps.grayscale(im)
		im = im.filter(ImageFilter.FIND_EDGES)

	if preset=='poster':
		im = ImageOps.posterize(im,3)

	if preset=='solar':
		im = ImageOps.solarize(im, threshold=80) 

	if preset=='blur':
		im = im.filter(ImageFilter.BLUR)
	
	if preset=='sepia':
		sepia = []
		r, g, b = (239, 224, 185)
		for i in range(255):
			sepia.extend((r*i/255, g*i/255, b*i/255))
		im = im.convert("L")
		im.putpalette(sepia)
		im = im.convert("RGB")

	im.save(outputfile)

        bucket_name = 'project-1-imagepro'

        client = s3_client()

        client.upload_file(inputfile, bucket_name, filename)
        client.upload_file(outputfile, bucket_name, outputfilename)

	return outputfilename

def handle_uploaded_file(f,preset):
	uploadfilename='media/' + f.name
	with open(uploadfilename, 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)

        outputfilename = applyfilter(f.name, preset)
	return outputfilename

def home(request):
        context = {}
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
                        preset=request.POST['preset']
			outputfilename = handle_uploaded_file(request.FILES['myfilefield'],
                                                              preset)
                        context['outputfilename'] = outputfilename
			return render_to_response('process.html',
                                                  context, 
                                                  context_instance=RequestContext(request))
	else:
		form = UploadFileForm() 
                print('No Posting Done')

        context['form'] = form

        # list all files in s3
        # connect to S3
        client = s3_client()

        # get all files from S3
        bucket_name = 'project-1-imagepro'        
        download_list = client.get_user_files(bucket_name)
        print('-----------')
        print(download_list)
        print('-----------')

        # if files exist on S3
        if(len(download_list) > 0):
                # convert contents to ascii
                temp = []
                for item in download_list:
                        temp.append(item.encode('ascii'))
                download_list = temp

                # add files to html context
                context['download_list'] = download_list
                print('Displaying download list')
                
                # download s3 files to local EC2 instance
                for item in download_list:
                        print(item)
                        client.download_from_s3(bucket_name, '/home/ec2-user/AWSImagePro/myapp/templates/static/downloads/' + item, item)
                        
        # render home page
        return render_to_response('home.html', context, 
                                  context_instance=RequestContext(request))

def process(request):
	return render_to_response('process.html', {})
