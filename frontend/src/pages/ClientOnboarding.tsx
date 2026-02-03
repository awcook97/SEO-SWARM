import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import toast from 'react-hot-toast'
import Card from '../components/Card'
import Input from '../components/Input'
import Button from '../components/Button'
import { onboardClient } from '../lib/api'
import { UserPlus, Loader2 } from 'lucide-react'

export default function ClientOnboarding() {
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    name: '',
    slug: '',
    website: '',
    crawlSite: false,
  })

  const onboardMutation = useMutation({
    mutationFn: onboardClient,
    onSuccess: () => {
      toast.success('Client onboarded successfully!')
      navigate('/')
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to onboard client')
    },
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!formData.name || !formData.slug) {
      toast.error('Name and slug are required')
      return
    }

    onboardMutation.mutate({
      name: formData.name,
      slug: formData.slug,
      website: formData.website || undefined,
      crawl_site: formData.crawlSite,
    })
  }

  const handleSlugify = () => {
    if (formData.name && !formData.slug) {
      const slug = formData.name
        .toLowerCase()
        .replace(/[^a-z0-9]+/g, '-')
        .replace(/(^-|-$)/g, '')
      setFormData({ ...formData, slug })
    }
  }

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Onboard New Client</h1>
        <p className="mt-2 text-gray-600">
          Create a new client workspace with scaffolded directories and files
        </p>
      </div>

      {/* Form */}
      <Card>
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Client Name */}
          <Input
            label="Client Name"
            placeholder="e.g., Acme HVAC Services"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            onBlur={handleSlugify}
            required
          />

          {/* Slug */}
          <Input
            label="Slug"
            placeholder="e.g., acme-hvac"
            value={formData.slug}
            onChange={(e) => setFormData({ ...formData, slug: e.target.value })}
            required
          />
          <p className="text-xs text-gray-500 -mt-4">
            URL-friendly identifier (lowercase, hyphens only)
          </p>

          {/* Website */}
          <Input
            label="Website URL (Optional)"
            type="url"
            placeholder="https://example.com"
            value={formData.website}
            onChange={(e) => setFormData({ ...formData, website: e.target.value })}
          />

          {/* Crawl Site Option */}
          <div className="flex items-center gap-3">
            <input
              type="checkbox"
              id="crawlSite"
              checked={formData.crawlSite}
              onChange={(e) => setFormData({ ...formData, crawlSite: e.target.checked })}
              className="h-4 w-4 rounded border-gray-300 text-primary-600 focus:ring-primary-500"
            />
            <label htmlFor="crawlSite" className="text-sm text-gray-700">
              Crawl and cache site HTML during setup
            </label>
          </div>

          {/* Actions */}
          <div className="flex gap-3">
            <Button
              type="submit"
              disabled={onboardMutation.isPending}
              className="flex-1"
            >
              {onboardMutation.isPending ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Onboarding...
                </>
              ) : (
                <>
                  <UserPlus className="mr-2 h-4 w-4" />
                  Onboard Client
                </>
              )}
            </Button>
            <Button
              type="button"
              variant="secondary"
              onClick={() => navigate('/')}
            >
              Cancel
            </Button>
          </div>
        </form>
      </Card>

      {/* Info Card */}
      <Card title="What happens during onboarding?">
        <ul className="space-y-2 text-sm text-gray-600">
          <li className="flex items-start gap-2">
            <span className="text-primary-600">•</span>
            <span>Creates directory structure under <code className="bg-gray-100 px-1 rounded">data/outputs/&lt;slug&gt;/</code></span>
          </li>
          <li className="flex items-start gap-2">
            <span className="text-primary-600">•</span>
            <span>Scaffolds template files: inputs.md, pages, articles, social, email</span>
          </li>
          <li className="flex items-start gap-2">
            <span className="text-primary-600">•</span>
            <span>Optionally crawls website and caches HTML for analysis</span>
          </li>
          <li className="flex items-start gap-2">
            <span className="text-primary-600">•</span>
            <span>Pre-fills inputs.md with detected NAP and service information</span>
          </li>
        </ul>
      </Card>
    </div>
  )
}
