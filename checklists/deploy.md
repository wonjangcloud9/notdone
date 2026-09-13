# Deploy evidence

A green build is evidence that the build is green.

## The only proof that counts

Request the live URL from outside the deployment, and show the status:

```bash
curl -s -o /dev/null -w '%{http_code} %{time_total}s\n' https://your-app.example.com/
```

A 200 from the real host, after the deploy finished. Not the preview you already had open, which may be serving the previous version from cache.

## Check the thing you changed

The homepage returning 200 says nothing about the endpoint you touched. Request that one:

```bash
curl -s https://your-app.example.com/api/the-thing-you-changed | head -c 400
```

## Deployment status is not serving status

Platform dashboards report whether the rollout finished, not whether the app answers. They disagree more often than you would like. Ask the app.

## Environment variables

A variable added to the dashboard is not a variable the running process has. New env values usually need a redeploy to take effect. Prove it from the running app — an endpoint that reports its config, or a log line — not from the settings page.

## Rolling back

Know the command before you need it, and say what it is. "We can roll back" is not a plan; the exact invocation is.
