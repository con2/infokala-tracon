{{/* Common labels applied to all resources this chart creates. */}}
{{- define "infokala.labels" -}}
stack: infokala
{{- end -}}

{{/* Pod selector labels, shared between Deployment and Service. */}}
{{- define "infokala.selectorLabels" -}}
stack: infokala
component: gunicorn
{{- end -}}

{{/* Name of the Secret the Deployment reads from -- either chart-owned or existingSecretName. */}}
{{- define "infokala.secretName" -}}
{{ .Values.existingSecretName | default "infokala" }}
{{- end -}}
