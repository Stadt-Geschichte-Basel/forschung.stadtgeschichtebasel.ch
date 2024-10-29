module Jekyll
  module SortEDTF
    def sort_edtf(array_of_strings)
      # Parse each string into a hash with numeric, original, and display representations
      parsed_dates = array_of_strings.map do |str|
        cleaned_str = str.gsub(/[Xx]/, '0') # Replace X/x with 0 for numeric comparison
        
        # Remove leading zeros for numeric value calculation
        numeric_value = if cleaned_str.start_with?('-')
                          cleaned_str.sub(/^-0+/, '-').to_i
                        else
                          cleaned_str.sub(/^0+/, '').to_i
                        end

        # Create a human-readable display format
        # For display format, we use the original string, just without leading zeros
        display_format = if str.start_with?('-')
                           "#{str[1..-1].sub(/^0+/, '')} v. Chr."  # For negative, remove minus and leading zeros for display
                         else
                           str.sub(/^0+/, '')  # Remove leading zeros for positive values
                         end

        # Return a hash with numeric, original, and display_format
        { numeric: numeric_value, original: str, display_format: display_format }
      end

      # Sort by the numeric representation
      sorted_dates = parsed_dates.sort_by { |date| date[:numeric] }

      # Return an array of "display_format:original" strings
      sorted_dates.map { |date| "#{date[:display_format]}:#{date[:original]}" }
    end
  end
end
  
Liquid::Template.register_filter(Jekyll::SortEDTF)