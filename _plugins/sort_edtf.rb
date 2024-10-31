module Jekyll
  module SortEDTF
    def clean_date_string(str)
      str.gsub(/[Xx]/, '0')
    end

    def compute_numeric_value(cleaned_str)
      numeric_str = if cleaned_str.start_with?('-')
                         cleaned_str.sub(/^-0+/, '-')
                       else
                         cleaned_str.sub(/^0+(?=\d)/, '')
                       end
    
      if numeric_str.match?(/^-?\d+$/)
        numeric_str.to_i
      else
        raise ArgumentError, "Invalid date format: #{cleaned_str}"
      end
    end

    def create_display_format(str)
      if str.start_with?('-')
        "#{str[1..-1].sub(/^0+/, '')} v. u. Z."
      else
        str.sub(/^0+(?=\d)/, '')
      end
    end

    def sort_edtf(array_of_strings)
      valid_dates = array_of_strings.reject { |str| str.strip.empty? }

      parsed_dates = valid_dates.map do |str|
      cleaned_str = clean_date_string(str)
      numeric_value = compute_numeric_value(cleaned_str)
      display_format = create_display_format(str)

      { numeric: numeric_value, original: str, display_format: display_format }
      end

      sorted_dates = parsed_dates.sort_by { |date| -date[:numeric] }
      sorted_dates.map { |date| "#{date[:display_format]}:#{date[:original]}" }
    end
  end
end
  
Liquid::Template.register_filter(Jekyll::SortEDTF)