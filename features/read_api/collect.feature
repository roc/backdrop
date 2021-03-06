@use_read_api_client
Feature: collect fields into grouped responses


    Scenario: should be able to collect on a key for grouped queries
         Given "licensing_2.json" is in "foo" bucket
          when I go to "/foo?collect=authority&group_by=licence_name"
          then I should get back a status of "200"
          and the "1st" result should have "authority" with item ""Westminster""
          and the "1st" result should have "authority" with item ""Camden""


    Scenario: should be able to collect on a key for period grouped queries
         Given "licensing_2.json" is in "foo" bucket
          when I go to "/foo?collect=authority&period=week&group_by=licence_name"
          then I should get back a status of "200"
          and the "1st" result should have "authority" with item ""Westminster""
          and the "1st" result should have "authority" with item ""Camden""


    Scenario: should not be able to collect on non grouped queries
         Given "licensing_2.json" is in "foo" bucket
          when I go to "/foo?collect=authority"
          then I should get back a status of "400"

    Scenario: should be able to collect false values
        Given "licensing_2.json" is in "foo" bucket
         when I go to "/foo?group_by=licence_name&filter_by=isPaymentRequired:false&collect=isPaymentRequired"
         then I should get back a status of "200"
         and the "1st" result should have "isPaymentRequired" with item "false"
