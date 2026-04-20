require "cgi"

module Jekyll
  module ExternalMetadataLinks
    URL_PATTERN = %r{(?:(?:https?://)|(?:www\.))[^\s<>()]+}.freeze
    EXTERNAL_LINK_ICON = " <svg class='bi icon-sprite' role='img' aria-label='Externer Link'>" \
                         "<use xlink:href='/assets/lib/cb-icons.svg#icon-external-link'/>" \
                         "</svg>"

    def format_external_metadata_links(input)
      text = input.to_s
      output = +""
      last_index = 0

      text.to_enum(:scan, URL_PATTERN).each do
        match = Regexp.last_match
        raw_url = match[0]
        url, trailing = split_trailing_punctuation(raw_url)

        output << text[last_index...match.begin(0)]
        output << build_external_link(url)
        output << trailing
        last_index = match.end(0)
      end

      output << text[last_index..]
      output
    end

    private

    def split_trailing_punctuation(url)
      trailing = +""
      cleaned_url = url.dup

      loop do
        if cleaned_url.end_with?("&#59")
          trailing.prepend("&#59")
          cleaned_url = cleaned_url[0...-4]
        elsif cleaned_url.match?(/[.,;:!?]\z/)
          trailing.prepend(cleaned_url[-1])
          cleaned_url = cleaned_url[0...-1]
        else
          break
        end
      end

      [cleaned_url, trailing]
    end

    def build_external_link(url)
      href = url.start_with?("www.") ? "https://#{url}" : url
      "<a href='#{CGI.escapeHTML(href)}' target='_blank' rel='noopener'>#{CGI.escapeHTML(url)}#{EXTERNAL_LINK_ICON}</a>"
    end
  end
end

Liquid::Template.register_filter(Jekyll::ExternalMetadataLinks)
