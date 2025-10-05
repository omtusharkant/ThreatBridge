from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.conf import settings
import json
from .models import LogEntry

# Create your views here.
def index(request):
	return render(request, 'log_collector/index.html')

@csrf_exempt
def log_collector(request):
    if request.method == 'POST':
        api_key = request.headers.get('X-API-KEY')
        if not api_key or api_key != getattr(settings, 'LOG_COLLECTOR_API_KEY', None):
            return HttpResponse('Invalid or missing API key', status=401)

        try:
            body = json.loads(request.body)
            log_entries = []

            if isinstance(body, dict):
                logs = body.get('logs')
                if not isinstance(logs, list):
                    return HttpResponseBadRequest('Missing or invalid "logs" in request body, expected a list.')
                
                for log_data in logs:
                    entry = LogEntry(
                        message=log_data.get('message'),
                        source=log_data.get('source'),
                        level=log_data.get('level')
                    )
                    log_entries.append(entry)
            
            elif isinstance(body, list):
                # Handle old format (list of strings)
                for log_str in body:
                    if isinstance(log_str, str):
                        parts = log_str.split(',', 4)
                        if len(parts) == 5:
                            _, _, source, level, message = parts
                            entry = LogEntry(
                                message=message.strip(),
                                source=source.strip(),
                                level=level.strip()
                            )
                            log_entries.append(entry)
            else:
                return HttpResponseBadRequest('Invalid request body format. Expected a JSON object with a "logs" key or a JSON list of log strings.')

            if log_entries:
                LogEntry.objects.bulk_create(log_entries)
                return JsonResponse({'status': 'success', 'message': f'{len(log_entries)} logs received and saved'})
            else:
                return HttpResponseBadRequest('No valid log entries found in the request.')

        except json.JSONDecodeError:
            return HttpResponseBadRequest('Invalid JSON')
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return HttpResponseBadRequest('Only POST method is allowed')

